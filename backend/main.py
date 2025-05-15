from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from typing import Optional

# Data Models
class HealthCheck(BaseModel):
    status: str
    version: str
    environment: Optional[str] = None

class Echo(BaseModel):
    message: str

app = FastAPI(
    title="Med Talk Buddy API",
    description="Medical Assistant API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Med Talk Buddy API"}

@app.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        environment="development"
    )

@app.post("/echo", response_model=Echo)
async def echo(data: Echo):
    """Echo back the received message"""
    return data

@app.get("/error-test")
async def error_test():
    """Test error handling"""
    raise HTTPException(status_code=400, detail="Test error response")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
