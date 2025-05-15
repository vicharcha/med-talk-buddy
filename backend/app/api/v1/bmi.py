from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import Dict, List, Optional, Any
from app.core.auth import get_current_user, optional_current_user
from app.core.firebase_admin import db
from app.models.models import BMIRecord
from datetime import datetime
import uuid

router = APIRouter()

def calculate_bmi(height_cm: float, weight_kg: float) -> dict:
    """
    Calculate BMI and determine category
    
    BMI Categories:
    - Underweight: < 18.5
    - Normal weight: 18.5 - 24.9
    - Overweight: 25 - 29.9
    - Obesity (Class 1): 30 - 34.9
    - Obesity (Class 2): 35 - 39.9
    - Extreme Obesity (Class 3): >= 40
    """
    try:
        # Calculate BMI: weight (kg) / height (m)^2
        height_m = height_cm / 100
        bmi = weight_kg / (height_m * height_m)
        bmi = round(bmi, 2)
        
        # Determine BMI category
        category = ""
        if bmi < 18.5:
            category = "Underweight"
        elif bmi >= 18.5 and bmi < 25:
            category = "Normal weight"
        elif bmi >= 25 and bmi < 30:
            category = "Overweight"
        elif bmi >= 30 and bmi < 35:
            category = "Obesity (Class 1)"
        elif bmi >= 35 and bmi < 40:
            category = "Obesity (Class 2)"
        else:
            category = "Extreme Obesity (Class 3)"
            
        return {
            "bmi_value": bmi,
            "bmi_category": category
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating BMI: {str(e)}")

@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_bmi_endpoint(
    height_cm: float = Body(..., gt=0),
    weight_kg: float = Body(..., gt=0),
    notes: Optional[str] = Body(None),
    current_user: Optional[Dict[str, Any]] = Depends(optional_current_user)
):
    """Calculate BMI and optionally save the record if user is logged in"""
    
    # Calculate BMI
    bmi_result = calculate_bmi(height_cm, weight_kg)
    
    # If user is logged in, save the record
    if current_user:
        user_id = current_user["uid"]
        record_id = str(uuid.uuid4())
        
        bmi_record = {
            "id": record_id,
            "user_id": user_id,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "bmi_value": bmi_result["bmi_value"],
            "bmi_category": bmi_result["bmi_category"],
            "date": datetime.now(),
            "notes": notes
        }
        
        # Store in Firestore
        db.collection("bmi_records").document(record_id).set(bmi_record)
        
        # Add record ID to result
        bmi_result["record_id"] = record_id
        bmi_result["saved"] = True
    else:
        bmi_result["saved"] = False
    
    # Add input values to result
    bmi_result["height_cm"] = height_cm
    bmi_result["weight_kg"] = weight_kg
    bmi_result["notes"] = notes
    
    return bmi_result

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_bmi_history(
    limit: int = Query(10, gt=0, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get BMI calculation history for the current user"""
    user_id = current_user["uid"]
    
    try:
        # Query Firestore for BMI records
        records_query = (
            db.collection("bmi_records")
            .where("user_id", "==", user_id)
            .order_by("date", direction="DESCENDING")
            .limit(limit)
        )
        
        records = []
        for doc in records_query.stream():
            record_data = doc.to_dict()
            # Convert datetime to isoformat for JSON serialization
            if isinstance(record_data.get("date"), datetime):
                record_data["date"] = record_data["date"].isoformat()
            records.append(record_data)
            
        return records
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving BMI history: {str(e)}")

@router.delete("/record/{record_id}", response_model=Dict[str, str])
async def delete_bmi_record(
    record_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a specific BMI record"""
    user_id = current_user["uid"]
    
    try:
        # Get the record
        record_ref = db.collection("bmi_records").document(record_id)
        record = record_ref.get()
        
        if not record.exists:
            raise HTTPException(status_code=404, detail="Record not found")
            
        record_data = record.to_dict()
        
        # Check if the record belongs to the user
        if record_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this record")
            
        # Delete the record
        record_ref.delete()
        
        return {"message": "BMI record deleted successfully"}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting BMI record: {str(e)}")
