from fastapi import APIRouter
from app.api.v1 import bmi, chat, vision, medical_records, users

api_router = APIRouter()

# Include all route modules
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(bmi.router, prefix="/bmi", tags=["bmi"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(medical_records.router, prefix="/medical-records", tags=["medical-records"])
