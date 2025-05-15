# Healthcare Service Documentation

## Overview

The `HealthcareService` class provides a set of methods for handling healthcare-related operations in the application. It interacts with Firebase services to store and retrieve data, process healthcare queries from users, and generate personalized health recommendations.

## Class: HealthcareService

A service class that handles healthcare-related operations integrated with Firebase.

### Methods

#### `process_healthcare_query(user_id: str, message: str) -> Dict[str, Any]`

Processes a healthcare query from a user and generates an appropriate response.

**Parameters:**
- `user_id` (str): The unique identifier of the user sending the query
- `message` (str): The healthcare query from the user

**Returns:**
- `Dict[str, Any]`: A dictionary containing both the user message and the bot response, with the following structure:
  ```python
  {
    "user_message": {
      "id": str,            # Unique message ID
      "user_id": str,       # User ID
      "message": str,       # Original user message
      "is_bot": False,      # Flag indicating this is a user message
      "timestamp": str      # ISO formatted timestamp
    },
    "bot_message": {
      "id": str,            # Unique message ID
      "user_id": str,       # User ID
      "message": str,       # Bot response
      "is_bot": True,       # Flag indicating this is a bot message
      "timestamp": str      # ISO formatted timestamp
    }
  }
  ```

**Behavior:**
1. Creates a unique ID and timestamp for the user's message
2. Analyzes the message content using keyword detection
3. Generates a relevant response based on healthcare keywords identified
4. Stores both messages in Firestore under the "chat_messages" collection
5. Formats timestamps for JSON serialization
6. Returns both messages with their metadata

**Response Categories:**
- Greetings: Responds to "hello", "hi", "hey", etc.
- COVID-19: Information about coronavirus when keywords like "covid", "coronavirus", "pandemic" are detected
- Headaches: Advice when "headache", "head", "pain", "ache" are mentioned
- Diet: Nutrition guidance when "diet", "nutrition", "food", "eating" are detected
- Exercise: Physical activity recommendations for "exercise", "workout", "physical activity"
- Sleep: Sleep health information for "sleep", "insomnia", "rest"
- Mental Health: Support for "stress", "anxiety", "mental health", "depression"
- Default: A general response for any other healthcare queries

**Example Usage:**
```python
user_id = "user123"
message = "I've been having frequent headaches, what should I do?"
response = await HealthcareService.process_healthcare_query(user_id, message)
```

#### `get_health_recommendations(user_id: str) -> List[Dict[str, Any]]`

Generates personalized health recommendations for a user based on their health data, particularly their BMI.

**Parameters:**
- `user_id` (str): The unique identifier of the user

**Returns:**
- `List[Dict[str, Any]]`: A list of recommendation objects with the following structure:
  ```python
  [
    {
      "id": str,            # Unique recommendation ID
      "category": str,      # Recommendation category (e.g., "General", "Nutrition")
      "title": str,         # Recommendation title
      "description": str,   # Detailed recommendation
      "priority": str       # Priority level ("Low", "Medium", "High")
    },
    # More recommendations...
  ]
  ```

**Behavior:**
1. Retrieves the user's most recent BMI record from Firestore
2. Generates general health recommendations applicable to all users
3. If BMI data is available, adds BMI-specific recommendations:
   - For underweight users: Nutrition advice for healthy weight gain
   - For overweight/obese users: Calorie management and increased physical activity
   - For normal weight users: Balanced diet maintenance
4. Adds mental health recommendations for all users
5. Returns the compiled list of personalized recommendations

**Example Usage:**
```python
user_id = "user123"
recommendations = await HealthcareService.get_health_recommendations(user_id)
```

## Firebase Integration

The service interacts with Firebase in the following ways:

1. **Firestore Database**:
   - Stores user messages and bot responses in the "chat_messages" collection
   - Each document contains message content, user ID, timestamp, and message type flag
   - Retrieves user's BMI records from the "bmi_records" collection for personalized recommendations

2. **Data Structure**:
   - Chat messages are stored with unique UUIDs as document IDs
   - Each message has fields for content, user ID, timestamp, and a boolean flag indicating if it's from the bot
   - BMI records are queried with filters on the user ID and ordered by date

## Implementation Notes

- The current query processing system uses a simple keyword-based approach
- In a production environment, this would be replaced with a more sophisticated AI model
- Timestamps are converted to ISO format strings for proper JSON serialization
- All database operations use Firebase's Firestore client from the `app.core.firebase_admin` module

## Usage Limitations

- This service provides general health information only
- Users should always be advised to consult healthcare professionals for specific medical advice
- The recommendations are simplified and would be more personalized in a production system
- No personal health information (PHI) should be stored without proper HIPAA compliance measures

## Future Enhancements

- Integration with specialized healthcare AI models
- More sophisticated natural language processing
- Integration with external healthcare APIs
- Expanded recommendation logic based on multiple health factors
- Analytics for tracking user health trends
