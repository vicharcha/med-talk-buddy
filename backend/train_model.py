
import os
import numpy as np
import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalModelTrainer:
    def __init__(self, max_words=10000, max_sequence_length=500):
        self.max_words = max_words
        self.max_sequence_length = max_sequence_length
        self.tokenizer = Tokenizer(num_words=max_words)
        self.model = None
        
    def load_mmmu_dataset(self, dataset_path):
        """Load dataset from MMMU repository"""
        try:
            logger.info(f"Loading MMMU dataset from {dataset_path}")
            dataset = load_dataset(dataset_path)
            
            questions = []
            answers = []
            
            # Extract questions and answers from the dataset
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
            dataset = load_dataset(dataset_path)
            
            questions = []
            answers = []
            
            # Extract questions and answers from the dataset
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
                questions, answers = self.load_mmmu_dataset(dataset_path)
            else:
                questions, answers = self.load_mmlu_dataset(dataset_path)
                
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
        padded_sequences = pad_sequences(sequences, maxlen=self.max_sequence_length)
        
        # Convert answers to one-hot encoding
        num_classes = len(unique_answers)
        encoded_answers_array = np.array(encoded_answers)
        one_hot_answers = keras.utils.to_categorical(encoded_answers_array, num_classes)
        
        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            padded_sequences, one_hot_answers, test_size=0.2, random_state=42
        )
        
        return X_train, X_val, y_train, y_val, num_classes, unique_answers
    
    def build_model(self, num_classes, embedding_dim=100):
        """Build the model architecture"""
        model = Sequential()
        model.add(Embedding(self.max_words, embedding_dim, input_length=self.max_sequence_length))
        model.add(Bidirectional(LSTM(128, return_sequences=True)))
        model.add(Bidirectional(LSTM(64)))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
        """Train the model"""
        if self.model is None:
            raise ValueError("Model not built. Call build_model first.")
        
        logger.info("Starting model training...")
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        logger.info("Model training completed")
        return history
    
    def save_model(self, model_path="model/medical_model.h5"):
        """Save the model to H5 format"""
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        self.model.save(model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Also save the tokenizer
        tokenizer_path = os.path.join(os.path.dirname(model_path), "tokenizer.pickle")
        import pickle
        with open(tokenizer_path, 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info(f"Tokenizer saved to {tokenizer_path}")

def main():
    # List of datasets to train on
    datasets = [
        "MMMU/MMMU/Biology",
        "MMMU/MMMU/Basic_Medical_Science",
        "MMMU/MMMU/Chemistry",
        "MMMU/MMMU/Clinical_Medicine",
        "cais/mmlu/college_medicine",
        "cais/mmlu/clinical_knowledge",
        "cais/mmlu/nutrition",
        "cais/mmlu/philosophy",
        "cais/mmlu/human_aging",
        "cais/mmlu/human_sexuality",
        "cais/mmlu/medical_genetics"
    ]
    
    # Train the model with a small subset for testing
    # Adjust max_words and max_sequence_length based on your hardware capabilities
    trainer = MedicalModelTrainer(max_words=20000, max_sequence_length=500)
    
    logger.info("Preparing data...")
    try:
        X_train, X_val, y_train, y_val, num_classes, unique_answers = trainer.prepare_data(datasets)
        
        logger.info(f"Building model with {num_classes} output classes")
        trainer.build_model(num_classes)
        
        logger.info("Training model...")
        trainer.train(X_train, y_train, X_val, y_val, epochs=5)
        
        logger.info("Saving model...")
        trainer.save_model("model/medical_model.h5")
        
        # Save answer mapping for inference
        import pickle
        with open("model/answer_mapping.pickle", "wb") as f:
            pickle.dump(unique_answers, f)
        
        logger.info("Model training completed successfully!")
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise

if __name__ == "__main__":
    main()
