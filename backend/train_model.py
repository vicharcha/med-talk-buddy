import os
import numpy as np
import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import logging
import pickle
from typing import Any, Tuple
from functools import partial

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TextTokenizer:
    """Simple tokenizer class to replace Keras Tokenizer"""
    def __init__(self, num_words=10000):
        self.num_words = num_words
        self.word_index = {}
        self.index_word = {}
        self.word_counts = {}

    def fit_on_texts(self, texts):
        # Count words
        for text in texts:
            for word in text.split():
                if word not in self.word_counts:
                    self.word_counts[word] = 0
                self.word_counts[word] += 1
        
        # Sort words by frequency
        sorted_words = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Create word indices
        for i, (word, _) in enumerate(sorted_words[:self.num_words-1]):
            self.word_index[word] = i + 1  # Reserve 0 for padding
            self.index_word[i + 1] = word
            
    def texts_to_sequences(self, texts):
        sequences = []
        for text in texts:
            seq = []
            for word in text.split():
                if word in self.word_index:
                    seq.append(self.word_index[word])
            sequences.append(seq)
        return sequences

class MedicalModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes):
        super(MedicalModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm1 = nn.LSTM(embed_dim, hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(hidden_size * 2, hidden_size // 2, batch_first=True, bidirectional=True)
        self.fc1 = nn.Linear(hidden_size, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x, training=True):
        x = self.embedding(x)
        x, _ = self.lstm1(x)  # First bidirectional LSTM
        x, _ = self.lstm2(x)  # Second bidirectional LSTM
        x = self.fc1(x[:, -1, :])  # Take the last timestep
        x = self.relu(x)
        if training:
            x = self.dropout(x)
        x = self.fc2(x)
        return x  # Return raw logits (CrossEntropyLoss will apply softmax)

class MedicalModelTrainer:
    def __init__(self, max_words=10000, max_sequence_length=500):
        self.max_words = max_words
        self.max_sequence_length = max_sequence_length
        self.tokenizer = TextTokenizer(num_words=max_words)
        self.model = None
        self.device = device

    def load_mmmu_dataset(self, dataset_path):
        """Load dataset from MMMU repository"""
        try:
            logger.info(f"Loading MMMU dataset from {dataset_path}")
            dataset = load_dataset("MMMU/MMMU", dataset_path)
            
            questions = []
            answers = []
            
            for item in dataset['train']:
                if 'question' in item and 'answer' in item:
                    questions.append(item['question'])
                    answers.append(item['answer'])
            
            return questions, answers
        except Exception as e:
            logger.error(f"Error loading MMMU dataset: {e}")
            return [], []

    def load_mmlu_dataset(self, dataset_path):
        """Load dataset from MMLU repository"""
        try:
            logger.info(f"Loading MMLU dataset from {dataset_path}")
            dataset = load_dataset("cais/mmlu", dataset_path)
            
            questions = []
            answers = []
            
            for split in ['train', 'validation', 'test']:
                if split in dataset:
                    for item in dataset[split]:
                        if 'question' in item and 'answer' in item:
                            questions.append(item['question'])
                            answers.append(item['answer'])
            
            return questions, answers
        except Exception as e:
            logger.error(f"Error loading MMLU dataset: {e}")
            return [], []

    def prepare_data(self, dataset_paths):
        """Load and prepare data from multiple datasets"""
        all_questions = []
        all_answers = []
        
        for dataset_path in dataset_paths:
            logger.info(f"Processing dataset: {dataset_path}")
            
            if "MMMU" in dataset_path:
                questions, answers = self.load_mmmu_dataset(dataset_path.split('/')[-1])
            else:
                questions, answers = self.load_mmlu_dataset(dataset_path.split('/')[-1])
                
            all_questions.extend(questions)
            all_answers.extend(answers)
        
        logger.info(f"Total questions collected: {len(all_questions)}")
        
        # Encode answers as integers
        unique_answers = list(set(all_answers))
        answer_to_id = {answer: idx for idx, answer in enumerate(unique_answers)}
        encoded_answers = [answer_to_id[answer] for answer in all_answers]
        
        # Fit tokenizer on questions
        self.tokenizer.fit_on_texts(all_questions)
        
        # Convert questions to sequences
        sequences = self.tokenizer.texts_to_sequences(all_questions)
        
        # Pad sequences to the same length
        def pad_sequence(sequence, maxlen):
            if len(sequence) > maxlen:
                return sequence[:maxlen]
            return sequence + [0] * (maxlen - len(sequence))
            
        padded_sequences = [pad_sequence(seq, self.max_sequence_length) for seq in sequences]
        padded_sequences = torch.tensor(padded_sequences, dtype=torch.long)
        
        # Convert answers to tensor
        encoded_answers = torch.tensor(encoded_answers, dtype=torch.long)
        
        # Split data into training and validation sets
        indices = np.random.permutation(len(padded_sequences))
        split_idx = int(0.8 * len(indices))
        train_indices = indices[:split_idx]
        val_indices = indices[split_idx:]
        
        X_train = padded_sequences[train_indices]
        X_val = padded_sequences[val_indices]
        y_train = encoded_answers[train_indices]
        y_val = encoded_answers[val_indices]
        
        return X_train, X_val, y_train, y_val, len(unique_answers), unique_answers

    def build_model(self, num_classes, embedding_dim=100):
        """Initialize model"""
        self.model = MedicalModel(
            vocab_size=self.max_words,
            embed_dim=embedding_dim,
            hidden_size=128,
            num_classes=num_classes
        ).to(self.device)
        logger.info(f"Model built with {num_classes} output classes")

    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
        """Train the model"""
        if self.model is None:
            raise ValueError("Model not initialized. Call build_model first.")
        
        logger.info("Starting model training...")
        
        # Create datasets and dataloaders
        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size)
        
        # Optimizer and loss
        optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        criterion = nn.CrossEntropyLoss()
        
        train_history = []
        for epoch in range(epochs):
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            # Training
            for inputs, targets in train_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(inputs, training=True)
                loss = criterion(outputs, targets)
                loss.backward()
                
                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                optimizer.step()
                
                train_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                train_total += targets.size(0)
                train_correct += (predicted == targets).sum().item()
            
            train_loss /= train_total
            train_accuracy = train_correct / train_total
            
            # Validation
            self.model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for inputs, targets in val_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs, training=False)
                    loss = criterion(outputs, targets)
                    
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs, 1)
                    val_total += targets.size(0)
                    val_correct += (predicted == targets).sum().item()
            
            val_loss /= val_total
            val_accuracy = val_correct / val_total
            
            logger.info(
                f"Epoch {epoch + 1}/{epochs} - "
                f"loss: {train_loss:.4f} - "
                f"accuracy: {train_accuracy:.4f} - "
                f"val_loss: {val_loss:.4f} - "
                f"val_accuracy: {val_accuracy:.4f}"
            )
            
            train_history.append({
                'train': {'loss': train_loss, 'accuracy': train_accuracy},
                'validation': {'loss': val_loss, 'accuracy': val_accuracy}
            })
        
        logger.info("Model training completed")
        return train_history

    def save_model(self, model_path="model/medical_model.pt"):
        """Save the model to PyTorch format"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        torch.save(self.model.state_dict(), model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save the tokenizer
        tokenizer_path = os.path.join(os.path.dirname(model_path), "tokenizer.pickle")
        with open(tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"Tokenizer saved to {tokenizer_path}")

def main():
    # List of datasets to train on
    datasets = [
        "MMMU/Biology",
        "MMMU/Basic_Medical_Science",
        "MMMU/Chemistry",
        "MMMU/Clinical_Medicine",
        "cais/mmlu/college_medicine",
        "cais/mmlu/clinical_knowledge",
        "cais/mmlu/nutrition",
        "cais/mmlu/philosophy",
        "cais/mmlu/human_aging",
        "cais/mmlu/human_sexuality",
        "cais/mmlu/medical_genetics"
    ]

    # Initialize trainer
    trainer = MedicalModelTrainer(max_words=20000, max_sequence_length=500)

    logger.info("Preparing data...")
    try:
        X_train, X_val, y_train, y_val, num_classes, unique_answers = trainer.prepare_data(datasets)
        
        logger.info(f"Building model with {num_classes} output classes")
        trainer.build_model(num_classes)
        
        logger.info("Training model...")
        trainer.train(X_train, y_train, X_val, y_val, epochs=5)
        
        logger.info("Saving model...")
        trainer.save_model("model/medical_model.pt")
        
        # Save answer mapping for inference
        with open("model/answer_mapping.pickle", "wb") as f:
            pickle.dump(unique_answers, f)
        
        logger.info("Model training completed successfully!")
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise

if __name__ == "__main__":
    main() 