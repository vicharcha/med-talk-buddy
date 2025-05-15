from typing import Dict, Any, List
import torch
from PIL import Image
import requests
from io import BytesIO
from transformers import pipeline
from app.core.config import settings
import os

class VisionService:
    def __init__(self):
        self.models = {}
        
    def _get_model(self, model_type: str):
        """Get or initialize a model for specific task"""
        if model_type not in self.models:
            try:
                model_path = os.path.join(settings.VISION_MODEL_PATH, model_type)
                if os.path.exists(model_path):
                    self.models[model_type] = pipeline(
                        "image-classification",
                        model=model_path,
                        device="cpu"  # Start with CPU for compatibility
                    )
                else:
                    # Use lightweight default models for initial setup
                    default_models = {
                        "xray": "google/vit-base-patch16-224",
                        "dermatology": "google/vit-base-patch16-224",
                        "pathology": "google/vit-base-patch16-224"
                    }
                    self.models[model_type] = pipeline(
                        "image-classification",
                        model=default_models.get(model_type, "google/vit-base-patch16-224"),
                        device="cpu"
                    )
            except Exception as e:
                print(f"Error loading model for {model_type}: {str(e)}")
                return None
        return self.models.get(model_type)

    async def analyze_image(
        self,
        image_url: str,
        analysis_type: str,
        additional_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Analyze medical images"""
        try:
            # Get model for analysis type
            model = self._get_model(analysis_type)
            if not model:
                return {
                    "error": f"Model not available for {analysis_type} analysis",
                    "details": "Please try again later"
                }

            # Download and process image
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Perform analysis
            results = model(image)

            # Process results based on analysis type
            processed_results = self._process_results(results, analysis_type)

            # Add recommendations
            recommendations = self._generate_recommendations(processed_results, analysis_type)

            return {
                "analysis_result": processed_results,
                "confidence_score": float(max(result["score"] for result in results)),
                "recommendations": recommendations
            }

        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return {
                "error": "Failed to analyze image",
                "details": str(e)
            }

    def _process_results(
        self,
        results: List[Dict[str, Any]],
        analysis_type: str
    ) -> Dict[str, Any]:
        """Process and format analysis results"""
        processed = {}
        
        if analysis_type == "xray":
            processed["findings"] = [
                {"condition": result["label"], "probability": result["score"]}
                for result in results
            ]
        elif analysis_type == "dermatology":
            processed["conditions"] = [
                {"diagnosis": result["label"], "confidence": result["score"]}
                for result in results
            ]
        elif analysis_type == "pathology":
            processed["observations"] = [
                {"finding": result["label"], "likelihood": result["score"]}
                for result in results
            ]

        return processed

    def _generate_recommendations(
        self,
        results: Dict[str, Any],
        analysis_type: str
    ) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = [
            "Please consult with a healthcare professional for accurate diagnosis",
            "This analysis is for informational purposes only"
        ]

        # Add type-specific recommendations
        if analysis_type == "xray":
            recommendations.append("Consider follow-up imaging if symptoms persist")
        elif analysis_type == "dermatology":
            recommendations.append("Document any changes in the appearance of the condition")
        elif analysis_type == "pathology":
            recommendations.append("Discuss these findings with your pathologist")

        return recommendations
