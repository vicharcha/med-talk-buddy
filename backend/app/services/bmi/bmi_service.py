from typing import List, Dict
from app.models.models import BMIRequest, BMIResponse

class BMIService:
    def __init__(self):
        self.bmi_categories = {
            'underweight': {'min': 0, 'max': 18.5},
            'normal': {'min': 18.5, 'max': 24.9},
            'overweight': {'min': 25, 'max': 29.9},
            'obese': {'min': 30, 'max': float('inf')}
        }

    def calculate_bmi(self, height: float, weight: float) -> float:
        """Calculate BMI using weight (kg) and height (m)"""
        return round(weight / (height * height), 2)

    def get_bmi_category(self, bmi: float) -> str:
        """Determine BMI category"""
        for category, range_values in self.bmi_categories.items():
            if range_values['min'] <= bmi < range_values['max']:
                return category
        return 'obese'  # Default for very high BMI values

    def get_recommendations(self, bmi: float, category: str, age: int, gender: str) -> List[str]:
        """Generate personalized recommendations based on BMI and other factors"""
        recommendations = []

        # Basic BMI-based recommendations
        if category == 'underweight':
            recommendations.extend([
                "Consider consulting a healthcare provider about healthy weight gain strategies",
                "Focus on nutrient-dense foods to support healthy weight gain",
                "Include protein-rich foods in your diet",
                "Consider strength training exercises to build muscle mass"
            ])
        elif category == 'normal':
            recommendations.extend([
                "Maintain your healthy lifestyle with balanced nutrition",
                "Regular physical activity is important for maintaining your healthy weight",
                "Continue with a balanced diet rich in fruits, vegetables, and whole grains",
                "Stay hydrated and maintain regular meal times"
            ])
        elif category == 'overweight':
            recommendations.extend([
                "Focus on portion control and mindful eating",
                "Incorporate more fruits, vegetables, and whole grains into your diet",
                "Aim for regular physical activity, at least 150 minutes per week",
                "Consider consulting a healthcare provider for personalized advice"
            ])
        elif category == 'obese':
            recommendations.extend([
                "Consult with a healthcare provider for personalized weight management strategies",
                "Focus on making sustainable lifestyle changes",
                "Consider working with a registered dietitian",
                "Start with gentle physical activities and gradually increase intensity"
            ])

        # Age-specific recommendations
        if age < 30:
            recommendations.append("Build healthy habits early to maintain long-term health")
        elif 30 <= age < 50:
            recommendations.append("Regular health screenings become increasingly important at this age")
        else:
            recommendations.append("Consider low-impact exercises that are gentle on joints")

        # Gender-specific recommendations
        if gender.lower() == 'female':
            recommendations.append("Ensure adequate calcium and iron intake for women's health")
        elif gender.lower() == 'male':
            recommendations.append("Include adequate protein for maintaining muscle mass")

        return recommendations

    def process_bmi_request(self, request: BMIRequest) -> BMIResponse:
        """Process a BMI calculation request and return detailed response"""
        # Calculate BMI
        bmi = self.calculate_bmi(request.height, request.weight)
        
        # Get category
        category = self.get_bmi_category(bmi)
        
        # Get recommendations
        recommendations = self.get_recommendations(
            bmi, 
            category, 
            request.age, 
            request.gender
        )
        
        return BMIResponse(
            bmi=bmi,
            category=category,
            recommendations=recommendations
        )

# Create singleton instance
bmi_service = BMIService()
