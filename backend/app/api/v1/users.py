from fastapi import APIRouter, HTTPException, Depends
from app.models.models import User, UserCreate, Token
from app.core.firebase_admin import verify_firebase_token, get_user_by_email
from typing import Optional

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    """
    Register a new user
    """
    try:
        # Here you would typically create a new user in Firebase
        # For now, return mock data
        return User(
            id="mock_id",
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(email: str, password: str):
    """
    Login user and return access token
    """
    try:
        # Here you would typically verify credentials with Firebase
        # For now, return mock token
        return Token(
            access_token="mock_token",
            token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=User)
async def get_current_user(token: str):
    """
    Get current user details
    """
    try:
        # Verify Firebase token
        decoded_token = verify_firebase_token(token)
        user = get_user_by_email(decoded_token["email"])
        return User(
            id=user["uid"],
            email=user["email"],
            full_name=user.get("displayName", ""),
            is_active=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
