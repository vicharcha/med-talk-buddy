from fastapi import APIRouter
from app.api.v1 import users, chat, bmi, medical_records

# Create API router
api_router = APIRouter()

# Include all API routes
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(bmi.router, prefix="/bmi", tags=["bmi"])
api_router.include_router(medical_records.router, prefix="/medical", tags=["medical_records"])
