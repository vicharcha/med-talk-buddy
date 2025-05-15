from fastapi import APIRouter, Depends, HTTPException, Body, Query, File, UploadFile
from typing import Dict, List, Optional, Any
from app.core.auth import get_current_user
from app.core.firebase_admin import db, bucket
from app.models.models import MedicalRecord, MedicalRecordType
from datetime import datetime
import uuid
import io

router = APIRouter()

@router.post("/records", response_model=Dict[str, Any])
async def create_medical_record(
    record_type: MedicalRecordType = Body(...),
    notes: str = Body(...),
    provider: Optional[str] = Body(None),
    metadata: Optional[Dict[str, Any]] = Body({}),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new medical record"""
    user_id = current_user["uid"]
    
    try:
        # Create a new record
        record_id = str(uuid.uuid4())
        now = datetime.now()
        
        medical_record = {
            "id": record_id,
            "user_id": user_id,
            "record_type": record_type.value,
            "record_date": now,
            "provider": provider,
            "notes": notes,
            "attachments": [],
            "metadata": metadata,
            "created_at": now,
            "updated_at": now
        }
        
        # Store record in Firestore
        db.collection("medical_records").document(record_id).set(medical_record)
        
        # Convert datetime objects to ISO format for response
        for key in ["record_date", "created_at", "updated_at"]:
            if isinstance(medical_record[key], datetime):
                medical_record[key] = medical_record[key].isoformat()
        
        return medical_record
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating medical record: {str(e)}")

@router.get("/records", response_model=List[Dict[str, Any]])
async def get_medical_records(
    record_type: Optional[MedicalRecordType] = Query(None),
    limit: int = Query(20, gt=0, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get medical records for the current user"""
    user_id = current_user["uid"]
    
    try:
        # Build query
        query = db.collection("medical_records").where("user_id", "==", user_id)
        
        # Add record type filter if provided
        if record_type:
            query = query.where("record_type", "==", record_type.value)
            
        # Execute query
        query = query.order_by("record_date", direction="DESCENDING").limit(limit)
        
        records = []
        for doc in query.stream():
            record_data = doc.to_dict()
            # Convert datetime objects to ISO format for response
            for key in ["record_date", "created_at", "updated_at"]:
                if isinstance(record_data.get(key), datetime):
                    record_data[key] = record_data[key].isoformat()
            records.append(record_data)
            
        return records
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving medical records: {str(e)}")

@router.get("/records/{record_id}", response_model=Dict[str, Any])
async def get_medical_record(
    record_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get a specific medical record"""
    user_id = current_user["uid"]
    
    try:
        # Get the record
        record_ref = db.collection("medical_records").document(record_id)
        record = record_ref.get()
        
        if not record.exists:
            raise HTTPException(status_code=404, detail="Record not found")
            
        record_data = record.to_dict()
        
        # Check if the record belongs to the user
        if record_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this record")
            
        # Convert datetime objects to ISO format for response
        for key in ["record_date", "created_at", "updated_at"]:
            if isinstance(record_data.get(key), datetime):
                record_data[key] = record_data[key].isoformat()
            
        return record_data
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving medical record: {str(e)}")

@router.put("/records/{record_id}", response_model=Dict[str, Any])
async def update_medical_record(
    record_id: str,
    notes: Optional[str] = Body(None),
    provider: Optional[str] = Body(None),
    metadata: Optional[Dict[str, Any]] = Body(None),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update a specific medical record"""
    user_id = current_user["uid"]
    
    try:
        # Get the record
        record_ref = db.collection("medical_records").document(record_id)
        record = record_ref.get()
        
        if not record.exists:
            raise HTTPException(status_code=404, detail="Record not found")
            
        record_data = record.to_dict()
        
        # Check if the record belongs to the user
        if record_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this record")
            
        # Prepare update data
        update_data = {"updated_at": datetime.now()}
        
        if notes is not None:
            update_data["notes"] = notes
            
        if provider is not None:
            update_data["provider"] = provider
            
        if metadata is not None:
            update_data["metadata"] = metadata
            
        # Update the record
        record_ref.update(update_data)
        
        # Get updated record
        updated_record = record_ref.get().to_dict()
        
        # Convert datetime objects to ISO format for response
        for key in ["record_date", "created_at", "updated_at"]:
            if isinstance(updated_record.get(key), datetime):
                updated_record[key] = updated_record[key].isoformat()
            
        return updated_record
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating medical record: {str(e)}")

@router.delete("/records/{record_id}", response_model=Dict[str, str])
async def delete_medical_record(
    record_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete a specific medical record"""
    user_id = current_user["uid"]
    
    try:
        # Get the record
        record_ref = db.collection("medical_records").document(record_id)
        record = record_ref.get()
        
        if not record.exists:
            raise HTTPException(status_code=404, detail="Record not found")
            
        record_data = record.to_dict()
        
        # Check if the record belongs to the user
        if record_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this record")
            
        # Delete any attachments from storage
        for attachment_path in record_data.get("attachments", []):
            try:
                blob = bucket.blob(attachment_path)
                blob.delete()
            except Exception as e:
                # Log error but continue with record deletion
                print(f"Error deleting attachment {attachment_path}: {str(e)}")
            
        # Delete the record
        record_ref.delete()
        
        return {"message": "Medical record deleted successfully"}
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting medical record: {str(e)}")

@router.post("/records/{record_id}/attachments", response_model=Dict[str, Any])
async def upload_attachment(
    record_id: str,
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Upload an attachment to a medical record"""
    user_id = current_user["uid"]
    
    try:
        # Get the record
        record_ref = db.collection("medical_records").document(record_id)
        record = record_ref.get()
        
        if not record.exists:
            raise HTTPException(status_code=404, detail="Record not found")
            
        record_data = record.to_dict()
        
        # Check if the record belongs to the user
        if record_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to modify this record")
            
        # Read file content
        content = await file.read()
        
        # Generate storage path
        file_ext = file.filename.split('.')[-1] if '.' in file.filename else ''
        attachment_id = str(uuid.uuid4())
        storage_path = f"medical_records/{user_id}/{record_id}/{attachment_id}.{file_ext}"
        
        # Upload to Firebase Storage
        blob = bucket.blob(storage_path)
        blob.upload_from_string(
            content,
            content_type=file.content_type
        )
        
        # Set public URL if needed
        # blob.make_public()
        # public_url = blob.public_url
        
        # Update record with attachment reference
        attachments = record_data.get("attachments", [])
        attachments.append(storage_path)
        
        record_ref.update({
            "attachments": attachments,
            "updated_at": datetime.now()
        })
        
        return {
            "message": "Attachment uploaded successfully",
            "attachment_path": storage_path,
            "filename": file.filename
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading attachment: {str(e)}")
