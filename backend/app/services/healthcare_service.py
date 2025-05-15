from typing import Dict, List, Optional, Any
from app.core.firebase_admin import db
import uuid
from datetime import datetime

class HealthcareService:
    """
    Service for healthcare-related operations interacting with Firebase.
    
    This service provides methods for processing healthcare queries and
    generating personalized health recommendations based on user data.
    """
    
    @staticmethod
    async def process_healthcare_query(user_id: str, message: str) -> Dict[str, Any]:
        """
        Process a healthcare query and generate a response.
        
        This method analyzes the user's message for healthcare-related keywords
        and provides relevant information. The conversation is stored in Firestore.
        
        In a production system, this would integrate with a healthcare AI model
        or external API for generating responses. This is a simplified placeholder.
        
        Args:
            user_id (str): The unique identifier of the user sending the query
            message (str): The healthcare query from the user
            
        Returns:
            Dict[str, Any]: A dictionary containing both the user message and bot response
                with their respective metadata (id, timestamp, etc.)
                
        Example:
            >>> response = await HealthcareService.process_healthcare_query("user123", "I have a headache")
            >>> print(response["bot_message"]["message"])
            "Headaches can be caused by various factors including stress..."
        """
        # Create a record of the user query
        message_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # This is where you would call an external AI service
        # For now, we'll use a simple rule-based response system
        
        # Simple keyword-based response generation
        response = ""
        if any(word in message.lower() for word in ["hello", "hi", "hey", "greetings"]):
            response = "Hello! How can I assist you with your healthcare needs today?"
        elif any(word in message.lower() for word in ["covid", "coronavirus", "pandemic"]):
            response = "COVID-19 is caused by the SARS-CoV-2 virus. Common symptoms include fever, cough, and fatigue. " \
                       "If you're experiencing symptoms, please consult a healthcare professional."
        elif any(word in message.lower() for word in ["headache", "head", "pain", "ache"]):
            response = "Headaches can be caused by various factors including stress, dehydration, lack of sleep, " \
                       "or underlying medical conditions. For persistent or severe headaches, please consult a doctor."
        elif any(word in message.lower() for word in ["diet", "nutrition", "food", "eating"]):
            response = "A balanced diet rich in fruits, vegetables, lean proteins, and whole grains is essential for good health. " \
                       "It's recommended to limit processed foods and sugary drinks."
        elif any(word in message.lower() for word in ["exercise", "workout", "physical activity"]):
            response = "Regular physical activity is crucial for maintaining good health. Aim for at least 150 minutes " \
                       "of moderate-intensity exercise per week, along with muscle-strengthening activities."
        elif any(word in message.lower() for word in ["sleep", "insomnia", "rest"]):
            response = "Adults should aim for 7-9 hours of quality sleep per night. Consistent sleep and wake times, " \
                       "a comfortable environment, and limiting screen time before bed can help improve sleep quality."
        elif any(word in message.lower() for word in ["stress", "anxiety", "mental health", "depression"]):
            response = "Mental health is as important as physical health. Regular exercise, adequate sleep, mindfulness " \
                       "practices, and seeking professional help when needed are all important for mental wellbeing."
        else:
            response = "I understand you're asking about health matters. For specific medical advice, it's best to " \
                       "consult with a qualified healthcare professional. Is there anything else I can help with?"
        
        # Store the conversation in Firestore
        user_message = {
            "id": message_id,
            "user_id": user_id,
            "message": message,
            "is_bot": False,
            "timestamp": timestamp
        }
        
        db.collection("chat_messages").document(message_id).set(user_message)
        
        # Create and store the bot response
        bot_message_id = str(uuid.uuid4())
        bot_timestamp = datetime.now()
        bot_message = {
            "id": bot_message_id,
            "user_id": user_id,
            "message": response,
            "is_bot": True,
            "timestamp": bot_timestamp
        }
        
        db.collection("chat_messages").document(bot_message_id).set(bot_message)
        
        # Convert timestamps for JSON serialization
        user_message["timestamp"] = user_message["timestamp"].isoformat()
        bot_message["timestamp"] = bot_message["timestamp"].isoformat()
        
        # Return the conversation
        return {
            "user_message": user_message,
            "bot_message": bot_message
        }
    
    @staticmethod
    async def get_health_recommendations(user_id: str) -> List[Dict[str, Any]]:
        """
        Generate health recommendations for a user based on their data.
        
        This method retrieves the user's BMI records from Firestore and generates
        personalized health recommendations. It provides general recommendations
        for all users and specific recommendations based on BMI category.
        
        In a production system, this would analyze user data and BMI records
        to provide more sophisticated personalized recommendations.
        
        Args:
            user_id (str): The unique identifier of the user
            
        Returns:
            List[Dict[str, Any]]: A list of recommendation objects, each containing:
                - id: Unique recommendation ID
                - category: Recommendation category (e.g., "Nutrition", "General")
                - title: Brief recommendation title
                - description: Detailed recommendation text
                - priority: Priority level ("Low", "Medium", "High")
                
        Example:
            >>> recommendations = await HealthcareService.get_health_recommendations("user123")
            >>> for rec in recommendations:
            ...     print(f"{rec['title']} - {rec['priority']} priority")
            "Stay Hydrated - Medium priority"
            "Regular Exercise - High priority"
        """
        # Get user's BMI records
        bmi_query = (
            db.collection("bmi_records")
            .where("user_id", "==", user_id)
            .order_by("date", direction="DESCENDING")
            .limit(1)
        )
        
        recommendations = []
        
        # Get the latest BMI record if available
        latest_bmi = None
        for doc in bmi_query.stream():
            latest_bmi = doc.to_dict()
            break
        
        # General recommendations
        recommendations.append({
            "id": str(uuid.uuid4()),
            "category": "General",
            "title": "Stay Hydrated",
            "description": "Drink at least 8 glasses of water daily to maintain proper hydration.",
            "priority": "Medium"
        })
        
        recommendations.append({
            "id": str(uuid.uuid4()),
            "category": "General",
            "title": "Regular Exercise",
            "description": "Aim for at least 30 minutes of moderate activity 5 days a week.",
            "priority": "High"
        })
        
        # Add BMI-specific recommendations if available
        if latest_bmi:
            bmi_value = latest_bmi.get("bmi_value")
            bmi_category = latest_bmi.get("bmi_category")
            
            if bmi_category == "Underweight":
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "category": "Nutrition",
                    "title": "Increase Caloric Intake",
                    "description": "Focus on nutrient-dense foods to gain weight healthily.",
                    "priority": "High"
                })
            elif bmi_category in ["Overweight", "Obesity (Class 1)", "Obesity (Class 2)", "Extreme Obesity (Class 3)"]:
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "category": "Nutrition",
                    "title": "Calorie Management",
                    "description": "Focus on portion control and a balanced diet to achieve a healthy weight.",
                    "priority": "High"
                })
                
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "category": "Exercise",
                    "title": "Increase Physical Activity",
                    "description": "Add more movement to your daily routine, including both cardio and strength training.",
                    "priority": "High"
                })
            else:  # Normal weight
                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "category": "Nutrition",
                    "title": "Maintain Balanced Diet",
                    "description": "Continue eating a varied diet rich in fruits, vegetables, lean proteins, and whole grains.",
                    "priority": "Medium"
                })
        
        # Mental health recommendation for everyone
        recommendations.append({
            "id": str(uuid.uuid4()),
            "category": "Mental Health",
            "title": "Stress Management",
            "description": "Incorporate stress-reduction techniques like meditation, deep breathing, or yoga into your routine.",
            "priority": "Medium"
        })
        
        return recommendations
