from fastapi import APIRouter, HTTPException
from app.models.models import BMIRequest, BMIResponse
from app.services.bmi import bmi_service
from typing import Dict, Any

router = APIRouter(
    tags=["BMI Calculator"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request - Invalid input parameters"},
        500: {"description": "Internal server error"}
    },
)

@router.post(
    "/bmi/calculate",
    response_model=BMIResponse,
    summary="Calculate BMI",
    description="""
    Calculate BMI (Body Mass Index) and get personalized recommendations.
    
    Features:
    * Calculates precise BMI value
    * Determines BMI category
    * Provides personalized recommendations based on:
        - BMI category
        - Age
        - Gender
    
    Note: BMI is a general indicator and should not replace professional medical advice.
    """,
    response_description="BMI calculation results with recommendations"
)
async def calculate_bmi(request: BMIRequest) -> BMIResponse:
    """
    Calculate BMI and get personalized health recommendations.

    Parameters:
    - **height**: Height in meters (e.g., 1.75)
    - **weight**: Weight in kilograms (e.g., 70)
    - **age**: Age in years
    - **gender**: Gender ('male' or 'female')

    Returns:
    - BMI value
    - BMI category
    - Personalized recommendations
    """
    try:
        # Validate input
        if request.height <= 0 or request.weight <= 0:
            raise HTTPException(
                status_code=400,
                detail="Height and weight must be positive numbers"
            )
        
        if request.age <= 0:
            raise HTTPException(
                status_code=400,
                detail="Age must be a positive number"
            )

        # Process BMI calculation
        response = bmi_service.process_bmi_request(request)
        return response

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating BMI: {str(e)}"
        )
