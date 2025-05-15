import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings
import os

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Failed to initialize Firebase: {str(e)}")
        # If we're in development mode, use mock Firebase
        if os.getenv("ENVIRONMENT") == "development":
            from app.core.mock_firebase import initialize_mock_firebase
            initialize_mock_firebase()
        else:
            raise e

def verify_firebase_token(token: str):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {str(e)}")

def get_user_by_email(email: str):
    """Get Firebase user by email"""
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        raise ValueError(f"User not found: {str(e)}")

def create_custom_token(uid: str):
    """Create a custom token for a user"""
    try:
        custom_token = auth.create_custom_token(uid)
        return custom_token
    except Exception as e:
        raise ValueError(f"Failed to create custom token: {str(e)}")
