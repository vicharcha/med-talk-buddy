#!/usr/bin/env python
# filepath: /home/kasinadhsarma/med-talk-buddy/backend/train_model.py

"""
This script trains a simple machine learning model for the MedTalkBuddy healthcare chatbot.
It creates a neural network for intent classification based on medical intents data.
"""

import os
import numpy as np
import pickle
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import tensorflow as tf
from pathlib import Path

# Initialize directory for model files
MODEL_DIR = Path(__file__).parent / "models"
MODEL_DIR.mkdir(exist_ok=True)

print("Initializing ML model training...")

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK resources...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load medical intents data
def load_medical_intents():
    # Default medical intents data
    custom_intents_path = MODEL_DIR / "medical_intents.json"
    if custom_intents_path.exists():
        try:
            with open(custom_intents_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading custom intents: {e}")
    
    # If no custom file or error loading, use default intents from the ML service
    app_dir = Path(__file__).parent / "app"
    sys_path_modified = False
    
    if not app_dir.exists():
        print(f"Warning: App directory not found at {app_dir}")
        # Try using relative import
        import sys
        sys.path.append(str(Path(__file__).parent))
        sys_path_modified = True
    
    try:
        from app.services.ml_service import MedicalMLService
        medical_intents = MedicalMLService().load_medical_intents()
        
        # Save the intents to a file for future use
        with open(custom_intents_path, 'w') as file:
            json.dump(medical_intents, file, indent=4)
            
        return medical_intents
    except ImportError as e:
        print(f"Error importing ML service: {e}")
        # Fallback to empty intents
        return {"intents": []}
    finally:
        if sys_path_modified:
            sys.path.pop()

# Clean and preprocess text
def clean_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Tokenize
    words = word_tokenize(text)
    
    # Remove stopwords and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    
    return words

# Main training function
def train_model():
    print("Loading medical intents data...")
    intents = load_medical_intents()
    
    if not intents.get("intents"):
        print("Error: No intents data available. Cannot train model.")
        return False
    
    print(f"Loaded {len(intents['intents'])} intent categories.")
    
    # Prepare training data
    words = []
    classes = []
    documents = []
    
    # Process each intent
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            # Clean and tokenize
            pattern_words = clean_text(pattern)
            
            # Add to words list
            words.extend(pattern_words)
            
            # Add to documents
            documents.append((pattern_words, intent["tag"]))
            
            # Add to classes list
            if intent["tag"] not in classes:
                classes.append(intent["tag"])
    
    # Remove duplicates and sort
    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))
    
    print(f"Unique tokens: {len(words)}")
    print(f"Intent classes: {len(classes)}")
    
    # Save words and classes
    with open(MODEL_DIR / "words.pkl", 'wb') as f:
        pickle.dump(words, f)
        
    with open(MODEL_DIR / "classes.pkl", 'wb') as f:
        pickle.dump(classes, f)
    
    # Create training data
    training = []
    
    # Create empty output row
    output_empty = [0] * len(classes)
    
    # Create bag of words for each pattern
    for doc in documents:
        # Initialize bag of words
        bag = []
        
        # List of tokenized words for the pattern
        pattern_words = doc[0]
        
        # Create bag of words array
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
        
        # Output is a '0' for each tag and '1' for current tag
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        
        training.append([bag, output_row])
    
    # Shuffle training data
    random.shuffle(training)
    
    # Convert to numpy arrays
    train_x = np.array([item[0] for item in training])
    train_y = np.array([item[1] for item in training])
    
    # Build neural network model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(tf.keras.layers.Dense(len(train_y[0]), activation='softmax'))
    
    # Compile model
    model.compile(loss='categorical_crossentropy', 
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), 
                  metrics=['accuracy'])
    
    # Train and save model
    print("Training model...")
    model.fit(train_x, train_y, epochs=200, batch_size=8, verbose=1)
    
    # Save model
    model.save(MODEL_DIR / "medical_model.h5")
    print(f"Model saved to {MODEL_DIR / 'medical_model.h5'}")
    
    # Evaluate model
    loss, accuracy = model.evaluate(train_x, train_y, verbose=0)
    print(f"Training accuracy: {accuracy*100:.2f}%")
    
    return True

if __name__ == "__main__":
    success = train_model()
    if success:
        print("Model training completed successfully!")
    else:
        print("Model training failed. Check the error messages above.")
