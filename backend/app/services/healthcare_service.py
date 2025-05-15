from typing import List, Dict, Any
from app.models.models import BMIRequest, BMIResponse

class HealthcareService:
    @staticmethod
    def calculate_bmi(data: BMIRequest) -> BMIResponse:
        """Calculate BMI and provide recommendations"""
        height_m = data.height
        weight_kg = data.weight
        
        # Calculate BMI
        bmi = weight_kg / (height_m * height_m)
        
        # Determine BMI category
        if bmi < 18.5:
            category = "Underweight"
            recommendations = [
                "Consider consulting a nutritionist",
                "Increase caloric intake with healthy foods",
                "Include protein-rich foods in your diet",
                "Start strength training exercises"
            ]
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
            recommendations = [
                "Maintain your current healthy lifestyle",
                "Regular exercise (150 minutes per week)",
                "Balanced diet with plenty of fruits and vegetables",
                "Regular health check-ups"
            ]
        elif 25 <= bmi < 30:
            category = "Overweight"
            recommendations = [
                "Increase physical activity",
                "Monitor portion sizes",
                "Focus on whole foods",
                "Consider consulting a healthcare provider"
            ]
        else:
            category = "Obese"
            recommendations = [
                "Consult a healthcare provider",
                "Create a structured weight loss plan",
                "Regular physical activity",
                "Consider working with a registered dietitian"
            ]
        
        # Adjust recommendations based on age
        if data.age >= 65:
            recommendations.append("Consult with healthcare provider before starting new exercise routine")
        
        return BMIResponse(
            bmi=round(bmi, 2),
            category=category,
            recommendations=recommendations
        )

    @staticmethod
    def validate_medical_record(record: Dict[str, Any]) -> bool:
        """Validate medical record data"""
        required_fields = ["user_id", "record_type", "date", "description"]
        return all(field in record for field in required_fields)
