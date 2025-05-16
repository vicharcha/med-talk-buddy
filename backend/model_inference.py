
import pickle
import numpy as np
import torch
import torch.nn as nn
from train_model import MedicalModel  # Import the model architecture
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalModelInference:
    def __init__(self, model_path="model/medical_model.pt", 
                 tokenizer_path="model/tokenizer.pickle",
                 answer_mapping_path="model/answer_mapping.pickle",
                 max_sequence_length=500):
        self.max_sequence_length = max_sequence_length
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None
        self.answer_mapping = None
        self.load_model(model_path, tokenizer_path, answer_mapping_path)
    
    def load_model(self, model_path, tokenizer_path, answer_mapping_path):
        """Load the trained model, tokenizer, and answer mapping"""
        try:
            logger.info(f"Loading model from {model_path}")
            # First load tokenizer to get vocab size
            with open(tokenizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            
            # Load answer mapping to get num_classes
            with open(answer_mapping_path, 'rb') as handle:
                self.answer_mapping = pickle.load(handle)
            
            # Initialize model with same architecture
            self.model = MedicalModel(
                vocab_size=self.tokenizer.num_words,
                embed_dim=100,
                hidden_size=128,
                num_classes=len(self.answer_mapping)
            ).to(self.device)
            
            # Load trained weights
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()  # Set to evaluation mode
            
            logger.info("Model, tokenizer, and answer mapping loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model resources: {e}")
            raise
    
    def preprocess_query(self, query):
        """Preprocess a single query for model input"""
        # Convert query to sequence
        sequence = self.tokenizer.texts_to_sequences([query])
        
        # Manual padding function
        def pad_sequence(seq, maxlen):
            if len(seq) > maxlen:
                return seq[:maxlen]
            return seq + [0] * (maxlen - len(seq))
        
        # Pad sequence to the required length
        padded_sequence = [pad_sequence(seq, self.max_sequence_length) for seq in sequence]
        
        # Convert to tensor
        return torch.tensor(padded_sequence, dtype=torch.long, device=self.device)
    
    def get_response(self, query, top_k=3):
        """Generate a response to a medical query"""
        if self.model is None or self.tokenizer is None or self.answer_mapping is None:
            logger.error("Model resources not loaded")
            return "I'm sorry, the medical model is not properly initialized."
        
        try:
            # Preprocess query
            processed_query = self.preprocess_query(query)
            
            # Get model predictions
            with torch.no_grad():
                logits = self.model(processed_query, training=False)
                probabilities = torch.softmax(logits, dim=-1)
            
            # Convert to numpy for easier handling
            predictions = probabilities.cpu().numpy()
            
            # Get top k answer indices
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            
            # Map indices to answers
            top_answers = [self.answer_mapping[idx] for idx in top_indices]
            top_probs = [predictions[0][idx] for idx in top_indices]
            
            # Format the response
            formatted_response = f"Based on your query: '{query}'\n\n"
            
            if top_probs[0] < 0.3:
                return "I'm not confident about the answer to this medical question. Please consult with a healthcare professional for accurate information."
            
            formatted_response += f"The most likely answer is: {top_answers[0]}"
            
            # Check if we want to include alternative answers
            if len(top_answers) > 1 and top_probs[1] > 0.2:
                formatted_response += f"\n\nAlternative possibilities include:"
                for i in range(1, min(len(top_answers), 3)):
                    if top_probs[i] > 0.1:  # Only include reasonably confident alternatives
                        formatted_response += f"\n- {top_answers[i]}"
            
            formatted_response += "\n\nRemember: This is AI-generated information and should not replace professional medical advice."
            
            return formatted_response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, there was an error processing your medical query."

# Example usage
if __name__ == "__main__":
    inference = MedicalModelInference()
    response = inference.get_response("What are the symptoms of diabetes?")
    print(response)
