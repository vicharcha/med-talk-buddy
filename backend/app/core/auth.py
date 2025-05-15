from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from app.core.firebase_admin import firebase_auth
from typing import Optional, Dict, Any

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Firebase token verification middleware
    """
    token = credentials.credentials
    try:
        # Verify Firebase JWT token
        decoded_token = firebase_auth.verify_id_token(token)
        
        # Get user data
        user_id = decoded_token.get("uid")
        user = firebase_auth.get_user(user_id)
        
        # Return user data
        return {
            "uid": user.uid,
            "email": user.email,
            "email_verified": user.email_verified,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "disabled": user.disabled
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )

def optional_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """
    Optional user verification - doesn't raise exception if no token
    """
    if not credentials:
        return None
        
    token = credentials.credentials
    try:
        # Verify Firebase JWT token
        decoded_token = firebase_auth.verify_id_token(token)
        
        # Get user data
        user_id = decoded_token.get("uid")
        user = firebase_auth.get_user(user_id)
        
        # Return user data
        return {
            "uid": user.uid,
            "email": user.email,
            "email_verified": user.email_verified,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "disabled": user.disabled
        }
    except Exception:
        return None
