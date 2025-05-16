from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import os
import uuid
import logging
import uvicorn
import google.generativeai as genai

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

# Configure Gemini AI
GOOGLE_API_KEY = "AIzaSyC-mMSX_CRu42U-ZhOtPdIfth4jKOSq-Ac"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Define contexts for different modes
chat_context = """You are MedTalkBuddy, an AI medical assistant trained to provide general medical information and advice. 
Remember to:
1. Always be professional and empathetic
2. Provide clear, accurate medical information based on current scientific knowledge
3. Include appropriate medical disclaimers when necessary
4. Recommend consulting healthcare professionals for specific diagnoses
5. Focus on evidence-based medical information
6. Never make definitive diagnoses
7. Use simple, understandable language
8. Provide emergency guidance when appropriate"""

predict_context = """You are MedTalkBuddy, an AI medical assistant trained to provide general medical information and advice.
Remember to:
1. Always be professional and empathetic
2. Provide clear, accurate medical information based on current scientific knowledge
3. Include appropriate medical disclaimers when necessary
4. Recommend consulting healthcare professionals for specific diagnoses
5. Focus on evidence-based medical information
6. Never make definitive diagnoses
7. Use simple, understandable language
8. Provide emergency guidance when appropriate

User has requested a symptom-based prediction. Analyze the symptoms provided and suggest possible conditions or advice, ensuring to include disclaimers."""

# Store conversation history (in-memory for demo purposes)
conversations: Dict[str, Dict] = {}

class MessageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    mode: str  # 'chat' or 'predict'

class MessageResponse(BaseModel):
    message: str
    conversation_id: str

@app.get("/")
def read_root():
    return {"message": "Welcome to MedTalkBuddy API"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/api/v1/chat/send", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    try:
        # Validate mode
        if request.mode not in ['chat', 'predict']:
            raise HTTPException(status_code=400, detail="Invalid mode. Choose 'chat' or 'predict'.")

        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())

        if conversation_id not in conversations:
            conversations[conversation_id] = {
                'messages': [],
                'chat': model.start_chat(history=[])
            }
            # Add greeting for new conversations
            greeting = ("Hello! I'm MedTalkBuddy, an AI trained to help answer medical questions. "
                        "While I can provide general medical information, please remember that I'm not a replacement "
                        "for professional medical advice. What medical question can I help you with today?")
            conversations[conversation_id]['messages'].append({"role": "assistant", "content": greeting})

        # Save user message
        conversations[conversation_id]['messages'].append({"role": "user", "content": request.message})

        # Select context based on mode
        if request.mode == 'chat':
            context = chat_context
        else:
            context = predict_context

        try:
            # Generate response using the conversation history and context
            chat = conversations[conversation_id]['chat']
            response = chat.send_message(
                context + "\n\nUser's message: " + request.message,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_DANGEROUS",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                ]
            )
            response_text = response.text

            # Add medical disclaimer for relevant keywords
            if any(word in request.message.lower() for word in ['emergency', 'urgent', 'severe', 'critical']):
                response_text += ("\n\n⚠️ IMPORTANT: If you're experiencing a medical emergency, "
                                  "please call emergency services (911 in the US) or visit the nearest emergency room immediately.")

            # Save bot response
            conversations[conversation_id]['messages'].append({"role": "assistant", "content": response_text})

            return MessageResponse(message=response_text, conversation_id=conversation_id)

        except Exception as e:
            logger.error(f"Model inference error: {e}")
            response_text = ("I apologize, but I encountered an error processing your question. "
                             "Please try rephrasing your question or ask something else.")
            return MessageResponse(message=response_text, conversation_id=conversation_id)

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Error processing your message")

@app.get("/api/v1/chat/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {"conversation_id": conversation_id, "messages": conversations[conversation_id]['messages']}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
