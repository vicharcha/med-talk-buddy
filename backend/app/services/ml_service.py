import os
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import tensorflow as tf
import pickle
from typing import Dict, Any, List, Tuple, Optional
import json
from pathlib import Path

# Initialize directory for model files
MODEL_DIR = Path(__file__).parent.parent.parent / "models"
MODEL_DIR.mkdir(exist_ok=True)

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class MedicalMLService:
    """Service for ML-based medical query processing"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to avoid loading model multiple times"""
        if cls._instance is None:
            cls._instance = super(MedicalMLService, cls).__new__(cls)
            cls._instance.initialize_model()
        return cls._instance
    
    def initialize_model(self):
        """Initialize or load the ML model and resources"""
        # Initialize the lemmatizer
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Load intents data
        self.intents = self.load_medical_intents()
        
        # Try to load the model if it exists, otherwise use rule-based responses
        self.model_path = MODEL_DIR / "medical_model.h5"
        self.words_path = MODEL_DIR / "words.pkl"
        self.classes_path = MODEL_DIR / "classes.pkl"
        
        if all(path.exists() for path in [self.model_path, self.words_path, self.classes_path]):
            try:
                # Load the saved model
                self.model = tf.keras.models.load_model(str(self.model_path))
                
                # Load words and classes
                with open(self.words_path, 'rb') as f:
                    self.words = pickle.load(f)
                    
                with open(self.classes_path, 'rb') as f:
                    self.classes = pickle.load(f)
                    
                print("Loaded existing ML model and resources")
                self.model_loaded = True
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model_loaded = False
        else:
            print("No trained model found. Using rule-based responses.")
            self.model_loaded = False
    
    def load_medical_intents(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load and return medical intents data for training or rule-based responses"""
        # Default medical intents data
        medical_intents = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["Hi", "Hello", "Hey", "Good morning", "Good afternoon", "Hi there", "Hello there"],
                    "responses": [
                        "Hello! I'm MedTalkBuddy, your healthcare assistant. How can I help you today?",
                        "Hi there! How can I assist with your health questions today?",
                        "Hello! I'm here to provide health information. What can I help you with?"
                    ]
                },
                {
                    "tag": "goodbye",
                    "patterns": ["Bye", "See you later", "Goodbye", "Thanks, bye", "Exit", "End"],
                    "responses": [
                        "Goodbye! Take care of your health.",
                        "Have a great day! Remember to stay healthy.",
                        "Goodbye! Feel free to return if you have more health questions."
                    ]
                },
                {
                    "tag": "thanks",
                    "patterns": ["Thank you", "Thanks", "That's helpful", "Appreciate it", "Thank you so much"],
                    "responses": [
                        "You're welcome! I'm happy to help with your health questions.",
                        "Glad I could assist! Remember, I provide general information, not medical advice.",
                        "You're welcome! Feel free to ask if you have more questions."
                    ]
                },
                {
                    "tag": "headache",
                    "patterns": ["I have a headache", "My head hurts", "Migraine", "Head pain", "Headache remedies"],
                    "responses": [
                        "Headaches can be caused by various factors including stress, dehydration, lack of sleep, or underlying medical conditions. Try resting in a dark room, staying hydrated, and taking over-the-counter pain relievers if appropriate. For persistent or severe headaches, please consult a healthcare professional.",
                        "I'm sorry to hear about your headache. Common remedies include rest, hydration, and over-the-counter pain relievers. If your headache is severe, sudden, or accompanied by other symptoms like fever, vision changes, or neck stiffness, please seek immediate medical attention.",
                        "Headaches have many causes. Simple remedies include rest, water, and OTC pain relievers. For recurring or severe headaches, please consult a doctor for proper diagnosis and treatment."
                    ]
                },
                {
                    "tag": "fever",
                    "patterns": ["I have a fever", "Temperature", "Feeling hot", "Chills and fever", "Reduce fever"],
                    "responses": [
                        "For adults, a fever is typically considered a temperature above 100.4°F (38°C). Rest, stay hydrated, and take acetaminophen or ibuprofen to reduce fever. Seek medical attention if your fever is very high (over 103°F/39.4°C), lasts more than three days, or is accompanied by severe symptoms like difficulty breathing, chest pain, or confusion.",
                        "Fever is your body's way of fighting infection. Stay hydrated, rest, and consider fever-reducing medications if uncomfortable. For high fevers, persistent fevers, or those accompanied by severe symptoms, please consult a healthcare provider.",
                        "To manage fever: rest, drink fluids, take acetaminophen or ibuprofen if needed, and dress lightly. See a doctor if fever is high, persistent, or accompanied by concerning symptoms."
                    ]
                },
                {
                    "tag": "cold_flu",
                    "patterns": ["I have a cold", "Flu symptoms", "Runny nose", "Sore throat", "Cough", "Congestion"],
                    "responses": [
                        "Cold and flu symptoms can include congestion, cough, sore throat, body aches, and sometimes fever. Rest, stay hydrated, and consider over-the-counter medications for symptom relief. Most colds resolve within 7-10 days. If symptoms worsen or last longer, consult a healthcare provider.",
                        "For cold or flu: rest, drink plenty of fluids, use saline nasal sprays for congestion, and take OTC medicines for fever and pain if needed. Honey can help with cough (for adults and children over 1 year). See a doctor if symptoms are severe or persist beyond a week.",
                        "Cold and flu treatment focuses on relief while your body fights the virus. Rest, fluids, and symptom-specific OTC remedies can help. Call a doctor if you have difficulty breathing, persistent fever, or symptoms that worsen after initial improvement."
                    ]
                },
                {
                    "tag": "diet",
                    "patterns": ["Healthy diet", "Nutrition advice", "What should I eat", "Diet recommendations", "Balanced diet"],
                    "responses": [
                        "A balanced diet includes plenty of fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, added sugars, and excessive salt. Stay hydrated by drinking water throughout the day. Consider consulting a dietitian for personalized nutrition advice.",
                        "For optimal health, focus on whole foods: fruits, vegetables, whole grains, lean proteins, and healthy fats. Minimize ultra-processed foods and sugary drinks. Portion control is important, as is staying hydrated with water.",
                        "Healthy eating means including a variety of nutrient-dense foods and limiting processed options. Aim for colorful fruits and vegetables, whole grains, lean proteins, and healthy fats while being mindful of portion sizes."
                    ]
                },
                {
                    "tag": "exercise",
                    "patterns": ["Exercise recommendations", "How much exercise", "Workout advice", "Physical activity", "Fitness tips"],
                    "responses": [
                        "Adults should aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous activity each week, plus muscle-strengthening activities twice weekly. Find activities you enjoy to make exercise sustainable. Always start gradually if you've been inactive.",
                        "Regular physical activity offers countless benefits including improved mood, better sleep, weight management, and reduced disease risk. Aim for both cardio and strength training. Even short bursts of activity throughout the day can be beneficial.",
                        "The best exercise is one you'll stick with consistently. Combine cardiovascular activities (walking, swimming, cycling) with strength training and flexibility work for a well-rounded fitness routine. Always warm up before and cool down after exercise."
                    ]
                },
                {
                    "tag": "sleep",
                    "patterns": ["Sleep problems", "Insomnia", "Can't sleep", "Sleep advice", "Better sleep", "Sleep hygiene"],
                    "responses": [
                        "Good sleep hygiene includes: consistent sleep schedule, comfortable bedroom environment, limiting screen time before bed, avoiding caffeine and large meals near bedtime, and establishing a relaxing pre-sleep routine. Most adults need 7-9 hours of quality sleep nightly.",
                        "For better sleep: maintain regular sleep-wake times, create a dark/quiet bedroom, avoid screens 1-2 hours before bed, limit caffeine and alcohol, exercise regularly (but not close to bedtime), and develop a relaxing bedtime routine.",
                        "If you struggle with sleep: try relaxation techniques, limit daytime napping, get natural light exposure during the day, and keep your bedroom for sleep only. If insomnia persists for more than a few weeks, consider consulting a healthcare provider."
                    ]
                },
                {
                    "tag": "stress",
                    "patterns": ["Stressed out", "Anxiety", "Stress management", "Feeling overwhelmed", "Reduce stress", "Calm anxiety"],
                    "responses": [
                        "Stress management techniques include: deep breathing exercises, regular physical activity, adequate sleep, mindfulness meditation, connecting with others, and setting realistic expectations. Find activities that help you relax and make time for them regularly.",
                        "To manage stress: identify your stress triggers, practice relaxation techniques (deep breathing, meditation, yoga), maintain healthy habits, connect with supportive people, and consider limiting media consumption. Professional help is available if stress becomes overwhelming.",
                        "Small stress-reducing activities can make a big difference: brief meditation sessions, short walks, journaling, or even just pausing for a few mindful breaths. For ongoing stress or anxiety that affects daily life, consider talking with a mental health professional."
                    ]
                },
                {
                    "tag": "blood_pressure",
                    "patterns": ["High blood pressure", "Hypertension", "Blood pressure readings", "Lower blood pressure", "BP management"],
                    "responses": [
                        "Healthy blood pressure is generally below 120/80 mmHg. Lifestyle changes to manage high blood pressure include: reducing sodium intake, regular exercise, maintaining healthy weight, limiting alcohol, not smoking, managing stress, and taking prescribed medications consistently.",
                        "High blood pressure often has no symptoms but can lead to serious health problems. Regular monitoring is important. Dietary approaches like the DASH diet (rich in fruits, vegetables, whole grains, and low-fat dairy) can help manage blood pressure.",
                        "For blood pressure management: maintain a healthy weight, exercise regularly, eat a heart-healthy diet, reduce sodium intake, limit alcohol, avoid tobacco, manage stress, and monitor your blood pressure at home if recommended by your doctor."
                    ]
                },
                {
                    "tag": "diabetes",
                    "patterns": ["Diabetes symptoms", "Blood sugar", "Diabetes management", "Glucose levels", "Diabetes diet"],
                    "responses": [
                        "Diabetes management includes: monitoring blood glucose levels, taking medications as prescribed, following a balanced meal plan, regular physical activity, and attending scheduled medical appointments. Work with healthcare providers to develop a personalized management plan.",
                        "Signs of diabetes can include increased thirst/hunger, frequent urination, unexplained weight loss, fatigue, blurred vision, and slow-healing sores. If you experience these symptoms, consult a healthcare provider for proper evaluation.",
                        "For diabetes diet considerations: focus on regular meal timing, portion control, plenty of non-starchy vegetables, moderate amounts of whole grains and lean proteins, and limited added sugars. A registered dietitian can help create a personalized meal plan."
                    ]
                },
                {
                    "tag": "heart_health",
                    "patterns": ["Heart disease", "Cardiovascular health", "Heart attack symptoms", "Chest pain", "Heart health tips"],
                    "responses": [
                        "Heart attack warning signs include chest pain/discomfort, shortness of breath, discomfort in other upper body areas, and sometimes nausea, lightheadedness, or cold sweat. If you experience these, call emergency services immediately - minutes matter!",
                        "For heart health: maintain healthy blood pressure and cholesterol levels, don't smoke, exercise regularly, eat a heart-healthy diet, maintain a healthy weight, manage stress, limit alcohol, and get enough quality sleep.",
                        "A heart-healthy diet emphasizes fruits, vegetables, whole grains, lean proteins (especially fish with omega-3s), nuts, seeds, and healthy oils while limiting saturated fats, trans fats, sodium, red meat, and added sugars."
                    ]
                },
                {
                    "tag": "bmi",
                    "patterns": ["Calculate BMI", "Body mass index", "Healthy weight", "Overweight", "BMI range"],
                    "responses": [
                        "BMI (Body Mass Index) is calculated as weight in kilograms divided by height in meters squared. Generally, a BMI under 18.5 is considered underweight, 18.5-24.9 is healthy weight, 25-29.9 is overweight, and 30+ is obese. However, BMI doesn't account for factors like muscle mass.",
                        "While BMI is a useful screening tool, it has limitations and doesn't directly measure body fat or account for age, sex, ethnicity, or muscle mass. For a more comprehensive health assessment, consider other factors alongside BMI.",
                        "For weight management, focus on sustainable lifestyle changes rather than quick fixes: balanced nutrition, portion awareness, regular physical activity, adequate sleep, stress management, and consistent habits."
                    ]
                }
            ]
        }
        
        # Check if a custom intents file exists and load it
        custom_intents_path = MODEL_DIR / "medical_intents.json"
        if custom_intents_path.exists():
            try:
                with open(custom_intents_path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading custom intents: {e}")
        
        # If no custom file or error loading, use default intents
        return medical_intents
    
    def clean_text(self, text: str) -> List[str]:
        """Clean and tokenize text for prediction"""
        # Convert to lowercase and remove punctuation
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenize
        words = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        
        return words
    
    def get_bag_of_words(self, text: str) -> np.ndarray:
        """Convert input text to bag of words format for model input"""
        if not self.model_loaded:
            return np.array([])
            
        # Clean and tokenize the text
        words_list = self.clean_text(text)
        
        # Create bag of words
        bag = [0] * len(self.words)
        for word in words_list:
            for i, w in enumerate(self.words):
                if w == word:
                    bag[i] = 1
                    
        return np.array([bag])
    
    def predict_intent(self, text: str) -> Tuple[str, float]:
        """Predict the intent of the user's message"""
        if not self.model_loaded:
            return self.rule_based_intent(text)
            
        # Get bag of words
        bow = self.get_bag_of_words(text)
        
        # Get prediction
        predictions = self.model.predict(bow)[0]
        
        # Get the highest probability
        max_prob = np.max(predictions)
        max_index = np.argmax(predictions)
        
        # Get the tag
        tag = self.classes[max_index]
        
        # Only return if probability is high enough
        if max_prob > 0.6:
            return tag, max_prob
        else:
            return self.rule_based_intent(text)
    
    def rule_based_intent(self, text: str) -> Tuple[str, float]:
        """Fallback rule-based intent classification"""
        text = text.lower()
        
        # Simple rule-based intent detection using keywords
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                pattern_words = set(pattern.lower().split())
                text_words = set(text.split())
                
                # Check if any words from the pattern are in the text
                if pattern_words.intersection(text_words):
                    # Calculate a simple confidence based on word overlap
                    confidence = len(pattern_words.intersection(text_words)) / len(pattern_words)
                    if confidence > 0.3:  # If at least 30% words match
                        return intent["tag"], confidence
        
        # If no intent is matched, return a general response
        return "general", 0.5
    
    def get_response(self, text: str) -> str:
        """Get a response based on the user's message"""
        # Get the intent
        tag, confidence = self.predict_intent(text)
        
        # Find the corresponding responses
        for intent in self.intents["intents"]:
            if intent["tag"] == tag:
                # Randomly select a response
                return np.random.choice(intent["responses"])
        
        # Fallback response if tag not found in intents
        return "I understand you're asking about health matters. For specific medical advice, it's best to consult with a qualified healthcare professional. Is there anything else I can help with?"


# Create an instance of the service
ml_service = MedicalMLService()

# Function to get a response for a message
async def get_ml_response(message: str) -> str:
    """Get an ML-generated response for a healthcare message"""
    return ml_service.get_response(message)
