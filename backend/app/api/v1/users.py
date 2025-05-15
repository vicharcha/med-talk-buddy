from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Dict, List, Optional, Any
from app.core.auth import get_current_user
from app.core.firebase_admin import db
from app.models.models import User
from firebase_admin import auth
import firebase_admin.exceptions

router = APIRouter()

@router.get("/me", response_model=Dict[str, Any])
async def read_users_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=Dict[str, Any])
async def update_user(
    display_name: Optional[str] = Body(None),
    photo_url: Optional[str] = Body(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user profile"""
    user_id = current_user["uid"]
    update_data = {}
    
    if display_name is not None:
        update_data["displayName"] = display_name
    
    if photo_url is not None:
        update_data["photoURL"] = photo_url
        
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
        
    try:
        # Update Firebase Auth user
        auth.update_user(
            user_id,
            **update_data
        )
        
        # Update Firestore document
        user_ref = db.collection("users").document(user_id)
        user_ref.update(update_data)
        
        # Get updated user
        updated_user = auth.get_user(user_id)
        
        return {
            "uid": updated_user.uid,
            "email": updated_user.email,
            "email_verified": updated_user.email_verified,
            "display_name": updated_user.display_name,
            "photo_url": updated_user.photo_url,
            "disabled": updated_user.disabled
        }
    except firebase_admin.exceptions.FirebaseError as e:
        raise HTTPException(status_code=400, detail=f"Firebase error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.delete("/me")
async def delete_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Delete current user"""
    user_id = current_user["uid"]
    
    try:
        # Delete user from Firebase Auth
        auth.delete_user(user_id)
        
        # Delete user data from Firestore
        batch = db.batch()
        
        # Delete user document
        user_ref = db.collection("users").document(user_id)
        batch.delete(user_ref)
        
        # Delete user's medical records
        records_query = db.collection("medical_records").where("user_id", "==", user_id).stream()
        for record in records_query:
            batch.delete(record.reference)
            
        # Delete user's chat history
        chats_query = db.collection("chat_messages").where("user_id", "==", user_id).stream()
        for chat in chats_query:
            batch.delete(chat.reference)
            
        # Delete BMI records
        bmi_query = db.collection("bmi_records").where("user_id", "==", user_id).stream()
        for bmi in bmi_query:
            batch.delete(bmi.reference)
            
        # Commit all deletions
        batch.commit()
        
        return {"message": "User successfully deleted"}
    except firebase_admin.exceptions.FirebaseError as e:
        raise HTTPException(status_code=400, detail=f"Firebase error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
