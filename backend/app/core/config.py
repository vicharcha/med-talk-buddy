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
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")
    FIREBASE_AUTH_DOMAIN: str = os.getenv("FIREBASE_AUTH_DOMAIN", "")
    FIREBASE_MESSAGING_SENDER_ID: str = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
    FIREBASE_APP_ID: str = os.getenv("FIREBASE_APP_ID", "")

    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()
