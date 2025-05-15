from typing import List, Dict, Any, Optional
from transformers import pipeline
import torch
from app.core.config import settings
import os

class MLService:
    def __init__(self):
        self.model = None

    def _get_model(self):
        """Get or initialize the language model"""
        if self.model is None:
            try:
                # Try to load local model first
                if os.path.exists(settings.SLM_MODEL_PATH):
                    self.model = pipeline(
                        "text-generation",
                        model=settings.SLM_MODEL_PATH,
                        device="cpu"  # Start with CPU for compatibility
                    )
                else:
                    # Use a smaller model for initial setup
                    self.model = pipeline(
                        "text-generation",
                        model="distilgpt2",  # Smaller model for faster loading
                        device="cpu"
                    )
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                return None
        return self.model

    async def generate_response(
        self,
        prompt: str,
        max_length: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using the language model"""
        try:
            model = self._get_model()
            if model is None:
                return "I apologize, but the AI model is currently unavailable. Please try again later."

            # Add medical context to prompt
            medical_prompt = (
                "You are a medical AI assistant. Provide accurate, professional "
                "medical information while being clear about limitations and "
                "encouraging consultation with healthcare providers when appropriate. "
                f"\n\nUser Query: {prompt}\n\nResponse:"
            )

            response = model(
                medical_prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95
            )

            return response[0]["generated_text"]

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I'm unable to generate a response at the moment. Please try again later."

    def validate_response(self, response: str) -> bool:
        """Validate the generated response"""
        # Add validation logic here
        return len(response) > 0 and not response.isspace()
