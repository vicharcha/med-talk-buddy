from fastapi import APIRouter, HTTPException, Depends
from app.models.models import ChatRequest, ChatResponse
from app.services.ml_service import MLService
from app.services.mcp_router import MCPRouter
from typing import Optional

router = APIRouter()
ml_service = MLService()
mcp_router = MCPRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Process a chat message and return a response
    """
    try:
        # Try local model first
        response = await ml_service.generate_response(request.message)
        
        # If local model fails or response is invalid, use MCP router
        if not ml_service.validate_response(response):
            mcp_response = await mcp_router.route_request(
                query=request.message,
                provider="openai"  # Default to OpenAI
            )
            response = mcp_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return ChatResponse(
            message=response,
            conversation_id=request.conversation_id or "new_conversation",
            additional_info=request.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
