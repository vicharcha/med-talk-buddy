import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import logging
import pickle
from typing import Any, Tuple, List, Dict
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import classification_report
import torch.nn.functional as F
from tokenizer import TextTokenizer  # Import our new SentencePiece tokenizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")


class SelfAttention(nn.Module):
    """Self attention module to focus on important tokens"""
    def __init__(self, hidden_size):
        super(SelfAttention, self).__init__()
        self.attention = nn.Linear(hidden_size, 1)

    def forward(self, x):
        weights = F.softmax(self.attention(x), dim=1)
        return torch.sum(weights * x, dim=1)


class MedicalModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_classes):
        super(MedicalModel, self).__init__()
        # Increase embedding dimension for better representation
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        
        # Add position embeddings
        self.position_embedding = nn.Parameter(torch.randn(1, 512, embed_dim))
        
        # Projection layers for residual connections
        self.proj1 = nn.Linear(embed_dim, hidden_size * 2)
        self.proj2 = nn.Linear(hidden_size * 2, hidden_size * 2)
        
        # Deeper LSTM architecture with residual connections
        self.lstm1 = nn.LSTM(embed_dim, hidden_size, num_layers=2, batch_first=True, bidirectional=True, dropout=0.2)
        self.lstm2 = nn.LSTM(hidden_size * 2, hidden_size, num_layers=2, batch_first=True, bidirectional=True, dropout=0.2)
        
        # Multiple attention heads
        self.attention1 = SelfAttention(hidden_size * 2)
        self.attention2 = SelfAttention(hidden_size * 2)
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(hidden_size * 2)
        self.norm2 = nn.LayerNorm(hidden_size * 2)
        
        # Deeper classifier
        self.fc1 = nn.Linear(hidden_size * 2, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, num_classes)
        
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()

    def forward(self, x, training=True):
        # Embedding with positional encoding
        x = self.embedding(x)
        x = x + self.position_embedding[:, :x.size(1), :]
        
        # First LSTM block with residual
        residual = self.proj1(x)  # Project to match dimensions
        x, _ = self.lstm1(x)
        x = self.norm1(x + residual)
        
        # Second LSTM block
        residual = self.proj2(x)  # Project to match dimensions
        x, _ = self.lstm2(x)
        x = self.norm2(x + residual)
        
        # Multi-head attention
        att1 = self.attention1(x)
        att2 = self.attention2(x)
        x = (att1 + att2) / 2
        
        # Classification layers
        x = self.fc1(x)
        x = self.relu(x)
        if training:
            x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        if training:
            x = self.dropout(x)
        x = self.fc3(x)
        
        return x


class MedicalModelTrainer:
    def __init__(self, vocab_size=20000, max_sequence_length=512):
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        # Initialize with SentencePiece tokenizer
        self.tokenizer = TextTokenizer(vocab_size=vocab_size, max_sequence_length=max_sequence_length)
        self.model = None
        self.device = device

    def load_mmmu_dataset(self, dataset_path):
        try:
            logger.info(f"Loading MMMU dataset from {dataset_path}")
            from datasets import load_dataset
            # Load all available splits
            dataset = load_dataset("MMMU/MMMU", dataset_path)
            questions = []
            answers = []
            
            # Process each available split
            for split in ['dev', 'validation', 'test']:
                if split in dataset:
                    split_data = dataset[split]
                    for item in split_data:
                        if 'question' in item and 'answer' in item:
                            # Preprocess questions to include domain context
                            question = f"[MED] {item['question']}"
                            questions.append(question)
                            answers.append(item['answer'])
            
            logger.info(f"Loaded {len(questions)} questions from MMMU dataset {dataset_path}")
            return questions, answers
        except Exception as e:
            logger.error(f"Error loading MMMU dataset: {e}")
            return [], []

    def load_mmlu_dataset(self, dataset_path):
        try:
            logger.info(f"Loading MMLU dataset from {dataset_path}")
            from datasets import load_dataset
            dataset = load_dataset("cais/mmlu", dataset_path)
            questions = []
            answers = []
            for split in ['train', 'validation', 'test']:
                if split in dataset:
                    for item in dataset[split]:
                        if 'question' in item and 'answer' in item:
                            # Add domain-specific prefix based on dataset type
                            if 'clinical' in dataset_path or 'medicine' in dataset_path:
                                prefix = '[MED]'
                            elif 'chemistry' in dataset_path:
                                prefix = '[CHEM]'
                            else:
                                prefix = '[DIAG]'
                            question = f"{prefix} {item['question']}"
                            questions.append(question)
                            answers.append(item['answer'])
            return questions, answers
        except Exception as e:
            logger.error(f"Error loading MMLU dataset: {e}")
            return [], []

    def prepare_data(self, dataset_paths):
        all_questions = []
        all_answers = []
        for dataset_path in dataset_paths:
            logger.info(f"Processing dataset: {dataset_path}")
            if "MMMU" in dataset_path:
                q, a = self.load_mmmu_dataset(dataset_path.split('/')[-1])
            else:
                q, a = self.load_mmlu_dataset(dataset_path.split('/')[-1])
            all_questions.extend(q)
            all_answers.extend(a)

        logger.info(f"Total questions collected: {len(all_questions)}")

        # Count answer frequencies
        answer_counts = {}
        for answer in all_answers:
            answer_counts[answer] = answer_counts.get(answer, 0) + 1
        
        # Filter out answers with too few samples (minimum 2)
        valid_answers = [ans for ans, count in answer_counts.items() if count >= 2]
        logger.info(f"Found {len(valid_answers)} valid answer classes with at least 2 samples")
        
        # Create filtered dataset
        filtered_questions = []
        filtered_answers = []
        for q, a in zip(all_questions, all_answers):
            if a in valid_answers:
                filtered_questions.append(q)
                filtered_answers.append(a)
        
        logger.info(f"Filtered dataset size: {len(filtered_questions)} questions")
        
        # Create answer mapping for valid answers only
        unique_answers = valid_answers
        answer_to_id = {a: i for i, a in enumerate(unique_answers)}
        encoded_answers = [answer_to_id[a] for a in filtered_answers]

        # Train tokenizer and encode sequences
        self.tokenizer.fit_on_texts(filtered_questions)
        sequences = self.tokenizer.texts_to_sequences(filtered_questions)

        # Convert to tensor format
        X = torch.tensor(sequences, dtype=torch.long)
        y = torch.tensor(encoded_answers, dtype=torch.long)

        # Stratified split
        sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_idx, val_idx in sss.split(X, y):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

        return X_train, X_val, y_train, y_val, len(unique_answers), unique_answers

    def build_model(self, num_classes, embedding_dim=256):  # Increased embedding dimension
        self.model = MedicalModel(
            vocab_size=self.vocab_size,
            embed_dim=embedding_dim,
            hidden_size=256,  # Increased hidden size
            num_classes=num_classes
        ).to(self.device)
        logger.info(f"Model built with {num_classes} output classes")

    def train(self, X_train, y_train, X_val, y_val, epochs=20, batch_size=32):
        if self.model is None:
            raise ValueError("Model not initialized. Call build_model first.")

        logger.info("Starting model training...")
        train_data = TensorDataset(X_train, y_train)
        val_data = TensorDataset(X_val, y_val)
        train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_data, batch_size=batch_size)

        # Calculate class weights for imbalanced dataset
        class_weights = torch.tensor([1.0 / (y_train.tolist().count(i) + 1) for i in range(len(set(y_train.tolist())))]).to(device)
        criterion = nn.CrossEntropyLoss(weight=class_weights)
        
        # Improved optimizer settings
        optimizer = optim.AdamW(  # Using AdamW instead of Adam
            self.model.parameters(),
            lr=2e-4,  # Lower learning rate
            weight_decay=0.01,  # Increased weight decay
            betas=(0.9, 0.999)  # Default betas
        )
        
        # Learning rate scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.2,
            patience=2,
            min_lr=1e-6
        )

        best_loss = float('inf')
        patience_counter = 0
        train_history = []

        for epoch in range(epochs):
            self.model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            # Training loop
            for inputs, targets in train_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                optimizer.zero_grad()
                outputs = self.model(inputs, training=True)
                loss = criterion(outputs, targets)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                optimizer.step()

                train_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                train_total += targets.size(0)
                train_correct += (predicted == targets).sum().item()

            train_loss /= train_total
            train_acc = train_correct / train_total

            # Validation loop
            self.model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            all_preds = []
            all_targets = []

            with torch.no_grad():
                for inputs, targets in val_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs, training=False)
                    loss = criterion(outputs, targets)
                    val_loss += loss.item() * inputs.size(0)
                    _, predicted = torch.max(outputs, 1)
                    val_total += targets.size(0)
                    val_correct += (predicted == targets).sum().item()
                    all_preds.extend(predicted.cpu().tolist())
                    all_targets.extend(targets.cpu().tolist())

            val_loss /= val_total
            val_acc = val_correct / val_total

            # Logging
            logger.info(
                f"Epoch {epoch + 1}/{epochs} - "
                f"loss: {train_loss:.4f}, acc: {train_acc:.4f} | "
                f"val_loss: {val_loss:.4f}, val_acc: {val_acc:.4f}"
            )

            # Early stopping and model saving
            if val_loss < best_loss:
                best_loss = val_loss
                patience_counter = 0
                self.save_model("model/medical_model.pt")
            else:
                patience_counter += 1

            if patience_counter >= 5:
                logger.info("Early stopping triggered.")
                break

            # Update learning rate
            scheduler.step(val_loss)
            
            # Save training history
            train_history.append({
                'train': {'loss': train_loss, 'accuracy': train_acc},
                'validation': {'loss': val_loss, 'accuracy': val_acc}
            })

            # Print detailed metrics
            if (epoch + 1) % 5 == 0 or epoch == 0 or epoch == epochs - 1:
                logger.info("\nDetailed Classification Report:")
                print(classification_report(all_targets, all_preds))

        logger.info("Model training completed")
        return train_history

    def save_model(self, model_path="model/medical_model.pt"):
        """Save the model, tokenizer, and other necessary files"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create model directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model state
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'vocab_size': self.vocab_size,
            'max_sequence_length': self.max_sequence_length
        }, model_path)
        logger.info(f"Model saved to {model_path}")

        # Save tokenizer
        tokenizer_path = os.path.join(os.path.dirname(model_path), "tokenizer.model")
        self.tokenizer.save(tokenizer_path)
        logger.info(f"Tokenizer saved to {tokenizer_path}")


def main():
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

    trainer = MedicalModelTrainer(vocab_size=32000, max_sequence_length=512)  # Increased vocab size
    logger.info("Preparing data...")

    try:
        X_train, X_val, y_train, y_val, num_classes, unique_answers = trainer.prepare_data(datasets)
        logger.info(f"Building model with {num_classes} output classes")
        trainer.build_model(num_classes)
        logger.info("Training model...")
        trainer.train(X_train, y_train, X_val, y_val, epochs=20)
        logger.info("Saving final model...")
        trainer.save_model("model/medical_model.pt")
        
        # Save answer mapping
        with open("model/answer_mapping.pickle", "wb") as f:
            pickle.dump(unique_answers, f)
        logger.info("Model training completed successfully!")

    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise


if __name__ == "__main__":
    main()
