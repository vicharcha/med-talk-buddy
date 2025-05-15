from fastapi import APIRouter, Depends, HTTPException
from app.models.models import BMIRequest, BMIResponse
from app.services.healthcare_service import HealthcareService

router = APIRouter()

@router.post("/calculate", response_model=BMIResponse)
async def calculate_bmi(data: BMIRequest):
    """
    Calculate BMI and provide recommendations based on the input data
    """
    try:
        result = HealthcareService.calculate_bmi(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
