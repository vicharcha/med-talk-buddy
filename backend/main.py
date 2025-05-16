
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uuid
import logging
import uvicorn
from model_inference import MedicalModelInference

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="MedTalkBuddy API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model if available
model = None
try:
    model = MedicalModelInference()
    logger.info("Medical model loaded successfully")
except Exception as e:
    logger.warning(f"Could not load medical model: {e}")
    logger.warning("The API will run without the medical model")

# Store conversation history (in-memory for demo purposes)
conversations = {}

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class MessageResponse(BaseModel):
    message: str
    conversation_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to MedTalkBuddy API"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/api/v1/chat/send", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Save user message
        conversations[conversation_id].append({"role": "user", "content": request.message})
        
        # Generate response
        if model:
            response_text = model.get_response(request.message)
        else:
            response_text = "I'm sorry, the medical model is currently unavailable. Please try again later."
        
        # Save bot response
        conversations[conversation_id].append({"role": "assistant", "content": response_text})
        
        return MessageResponse(message=response_text, conversation_id=conversation_id)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing your message")

@app.get("/api/v1/chat/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {"conversation_id": conversation_id, "messages": conversations[conversation_id]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
