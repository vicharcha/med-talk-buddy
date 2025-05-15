from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class BMIRequest(BaseModel):
    height: float = Field(..., description="Height in meters")
    weight: float = Field(..., description="Weight in kilograms")
    age: int = Field(..., description="Age in years")
    gender: str = Field(..., description="Gender (male/female)")

class BMIResponse(BaseModel):
    bmi: float
    category: str
    recommendations: List[str]

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    additional_info: Optional[Dict[str, Any]] = None

class MedicalRecord(BaseModel):
    id: str
    user_id: str
    record_type: str
    date: datetime
    description: str
    attachments: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class VisionAnalysisRequest(BaseModel):
    image_url: str
    analysis_type: str = Field(..., description="Type of analysis: xray/dermatology/pathology")
    additional_info: Optional[Dict[str, Any]] = None

class VisionAnalysisResponse(BaseModel):
    analysis_result: Dict[str, Any]
    confidence_score: float
    recommendations: Optional[List[str]] = None
