from pydantic import BaseModel, Field, EmailStr
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserCreate(UserBase):
    """User creation model"""
    password: str


class UserInDB(UserBase):
    """User in database model"""
    uid: str
    email_verified: bool = False
    disabled: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None


class User(UserBase):
    """User response model"""
    uid: str
    email_verified: bool = False


class MedicalRecordType(str, Enum):
    """Types of medical records"""
    CONSULTATION = "consultation"
    LAB_RESULT = "lab_result"
    PRESCRIPTION = "prescription"
    VITAL_SIGNS = "vital_signs"
    MEDICAL_HISTORY = "medical_history"


class MedicalRecord(BaseModel):
    """Medical record model"""
    id: Optional[str] = None
    user_id: str
    record_type: MedicalRecordType
    record_date: datetime
    provider: Optional[str] = None
    notes: str
    attachments: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = {}
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ChatMessage(BaseModel):
    """Chat message model"""
    id: Optional[str] = None
    user_id: str
    message: str
    is_bot: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = {}


class BMIRecord(BaseModel):
    """BMI calculation record"""
    id: Optional[str] = None
    user_id: str
    height_cm: float
    weight_kg: float
    bmi_value: float
    bmi_category: str
    date: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
