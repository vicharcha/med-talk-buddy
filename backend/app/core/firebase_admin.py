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
    # Skip Firebase initialization and use mock implementations
    print("Using mock Firebase services as requested")
    from app.core.mock_firebase import MockFirestore, MockStorage, MockAuth
    return {
        'db': MockFirestore(),
        'bucket': MockStorage(),
        'auth': MockAuth()
    }

# Export Firebase services
firebase_services = initialize_firebase_admin()
db = firebase_services['db']
bucket = firebase_services['bucket']
firebase_auth = firebase_services['auth']
