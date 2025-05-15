import os
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
from dotenv import load_dotenv
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Function to initialize Firebase Admin SDK
def initialize_firebase_admin():
    """Initialize Firebase Admin SDK for server-side operations"""
    try:
        # Path to service account key file
        cred_path = os.environ.get('FIREBASE_ADMIN_CREDENTIALS_PATH',
                                 str(Path(__file__).parents[2] / 'healthcare-77135-firebase-adminsdk-fbsvc-0e40ca9a7b.json'))
        
        # Initialize Firebase Admin with credentials
        cred = credentials.Certificate(cred_path)
        firebase_app = firebase_admin.initialize_app(cred)
        
        # Initialize Firestore, Storage, and Auth
        db = firestore.client()
        bucket = storage.bucket(f"{cred.project_id}.appspot.com")
        
        print("Firebase Admin SDK initialized successfully")
        return {
            'db': db,
            'bucket': bucket,
            'auth': auth,
            'app': firebase_app
        }
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        print("Falling back to mock implementations")
        from app.core.mock_firebase import MockFirestore, MockStorage, MockAuth
        return {
            'db': MockFirestore(),
            'bucket': MockStorage(),
            'auth': MockAuth(),
            'app': None
        }

# Export Firebase services
firebase_services = initialize_firebase_admin()
db = firebase_services['db']
bucket = firebase_services['bucket']
firebase_auth = firebase_services['auth']
firebase_app = firebase_services.get('app')
