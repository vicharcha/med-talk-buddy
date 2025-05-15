import os
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    """Application settings"""
    # API Configuration
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key-for-dev-only")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server default port
        "http://localhost:5174",
        "http://localhost:3000",
        "http://localhost:8080",  # Current frontend port
        "https://healthcare-77135.web.app",
        "https://healthcare-77135.firebaseapp.com"
    ]
    
    # Firebase Configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "healthcare-77135")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "healthcare-77135.appspot.com")
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "AIzaSyDH687LJ8huxt_zpE4TYWqB9OsCLTH4HDw")
    FIREBASE_AUTH_DOMAIN: str = os.getenv("FIREBASE_AUTH_DOMAIN", "healthcare-77135.firebaseapp.com")
    FIREBASE_MESSAGING_SENDER_ID: str = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "867221601164")
    FIREBASE_APP_ID: str = os.getenv("FIREBASE_APP_ID", "1:867221601164:web:e094a34d9f052d58d2f41c")

    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()
