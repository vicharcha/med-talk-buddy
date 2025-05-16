
from fastapi import APIRouter, HTTPException, Body
from app.models.models import ChatRequest, ChatResponse, ChatMessage
from app.services.chat.medical_chat import MedicalChatService
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/chat",
    tags=["Medical Chat"],
    responses={404: {"description": "Not found"}},
)

chat_service = MedicalChatService()

@router.post(
    "/send",
    response_model=ChatResponse,
    summary="Send a message to MedTalkBuddy",
    description="""
    Send a message to the AI medical assistant and get a response.
    
    The assistant has knowledge in:
    - Basic Medical Science
    - Clinical Medicine
    - Biology
    - Chemistry
    - Clinical Knowledge
    - College Medicine
    - Medical Genetics
    - Nutrition
    - Philosophy
    - Human Aging
    - Human Sexuality
    """
)
async def send_message(
    request: ChatRequest = Body(
        ...,
        example={
            "message": "What are the symptoms of diabetes?",
            "conversation_id": None,
            "context": None
        }
    )
):
    """
    Send a message to MedTalkBuddy and get an AI-powered medical response.
    """
    try:
        response = await chat_service.generate_response(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

@router.get(
    "/health",
    summary="Check chat service health",
    description="Check if the medical chat service is operational"
)
async def chat_health_check():
    """Check if the chat service is operational"""
    try:
        health_status = {
            "status": "healthy" if chat_service.chat is not None else "unavailable",
            "timestamp": datetime.utcnow().isoformat(),
            "model_info": {
                "name": chat_service.model_name,
                "device": chat_service.device
            }
        }
        return health_status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat service health check failed: {str(e)}"
        )
