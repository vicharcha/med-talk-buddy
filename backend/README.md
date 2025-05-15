# Healthcare ChatBot Backend

This is the backend API for the Healthcare ChatBot application, built with FastAPI and Firebase.

## Features

- User authentication via Firebase Auth
- Chat functionality with healthcare-focused AI responses
- BMI calculation and history tracking
- Medical records management
- Health recommendations

## Tech Stack

- FastAPI - High-performance Python web framework
- Firebase Admin SDK - For server-side operations
- Firestore - NoSQL document database
- Firebase Authentication - For user management
- Firebase Storage - For storing attachments and files

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Firebase project with Firestore and Authentication enabled
- Firebase service account credentials

### Setup Steps

1. Clone the repository (if not already done)

2. Navigate to the backend directory:
   ```
   cd backend
   ```

3. Run the initialization script:
   ```
   ./init.sh
   ```
   This script will:
   - Create a virtual environment
   - Install dependencies
   - Set up environment files
   - Help configure Firebase credentials

4. Edit the `.env` file with your Firebase configuration details

5. Download your Firebase service account key:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file securely

6. Run the Firebase credentials setup script:
   ```
   ./setup_firebase_credentials.sh
   ```
   Follow the prompts to set up your Firebase service account.

### Running the Backend

1. Activate the virtual environment (if not already activated):
   ```
   source venv/bin/activate
   ```

2. Start the FastAPI server:
   ```
   python -m uvicorn main:app --reload
   ```

3. The API will be available at:
   - API: http://localhost:8000/api/v1/
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- All endpoints are protected with Firebase Authentication
- Include the Firebase ID token in the Authorization header:
  ```
  Authorization: Bearer <firebase-id-token>
  ```

### Main Endpoints

- `/api/v1/users/me` - User profile operations
- `/api/v1/chat/messages` - Chat functionality
- `/api/v1/chat/recommendations` - Health recommendations
- `/api/v1/bmi/calculate` - BMI calculations
- `/api/v1/bmi/history` - BMI history
- `/api/v1/medical/records` - Medical records management

## Deployment

For production deployment:

1. Set `DEBUG=False` in the `.env` file
2. Generate a strong `SECRET_KEY`
3. Configure CORS settings appropriately in `config.py`
4. Use a production ASGI server like Uvicorn with Gunicorn

## License

This project is part of the Healthcare ChatBot application.
