from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Dict, List, Optional, Any
from app.core.auth import get_current_user
from app.core.firebase_admin import db
from app.models.models import ChatMessage
from app.services.healthcare_service import HealthcareService
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/messages", response_model=Dict[str, Any])
async def create_message(
    message: str = Body(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new user message and get bot response"""
    user_id = current_user["uid"]
    
    try:
        # Use healthcare service to process the message
        result = await HealthcareService.process_healthcare_query(user_id, message)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating message: {str(e)}")

@router.get("/messages", response_model=List[Dict[str, Any]])
async def get_messages(
    limit: int = Query(20, gt=0, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get chat message history for the current user"""
    user_id = current_user["uid"]
    
    try:
        # Query Firestore for messages
        messages_query = (
            db.collection("chat_messages")
            .where("user_id", "==", user_id)
            .order_by("timestamp", direction="DESCENDING")
            .limit(limit)
        )
        
        messages = []
        for doc in messages_query.stream():
            message_data = doc.to_dict()
            # Convert timestamp to isoformat for JSON serialization
            if isinstance(message_data.get("timestamp"), datetime):
                message_data["timestamp"] = message_data["timestamp"].isoformat()
            messages.append(message_data)
            
        # Return messages in chronological order
        return sorted(messages, key=lambda x: x["timestamp"])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")

@router.delete("/messages", response_model=Dict[str, str])
async def delete_all_messages(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete all chat messages for the current user"""
    user_id = current_user["uid"]
    
    try:
        # Query all messages for the user
        messages_query = db.collection("chat_messages").where("user_id", "==", user_id).stream()
        
        # Delete in batches (Firestore has limits on batch operations)
        batch = db.batch()
        count = 0
        
        for doc in messages_query:
            batch.delete(doc.reference)
            count += 1
            
            # Firestore allows up to 500 operations in a batch
            if count >= 500:
                batch.commit()
                batch = db.batch()
                count = 0
                
        # Commit any remaining deletes
        if count > 0:
            batch.commit()
            
        return {"message": "All chat messages deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting messages: {str(e)}")
        
@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_health_recommendations(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get personalized health recommendations for the current user"""
    user_id = current_user["uid"]
    
    try:
        # Get recommendations from the healthcare service
        recommendations = await HealthcareService.get_health_recommendations(user_id)
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving health recommendations: {str(e)}")
