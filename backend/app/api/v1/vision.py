from fastapi import APIRouter, HTTPException, Depends
from app.models.models import VisionAnalysisRequest, VisionAnalysisResponse
from app.services.vision_service import VisionService

router = APIRouter()
vision_service = VisionService()

@router.post("/analyze", response_model=VisionAnalysisResponse)
async def analyze_image(request: VisionAnalysisRequest):
    """
    Analyze medical images using vision models
    """
    try:
        result = await vision_service.analyze_image(
            image_url=request.image_url,
            analysis_type=request.analysis_type,
            additional_info=request.additional_info
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return VisionAnalysisResponse(
            analysis_result=result["analysis_result"],
            confidence_score=result["confidence_score"],
            recommendations=result.get("recommendations", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
