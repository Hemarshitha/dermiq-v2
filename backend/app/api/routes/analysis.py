"""Skin Analysis API"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
import shutil

router = APIRouter()

class AnalysisResponse(BaseModel):
    skin_type: str
    concerns: List[str]
    acne_severity: str
    pigmentation: str
    confidence: float
    recommendations: List[str]

@router.post("/analyze-image", response_model=AnalysisResponse)
async def analyze_skin_image(
    file: UploadFile = File(...),
    req: Request = None
):
    """Analyze facial skin image"""
    try:
        # Validate file
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Please upload an image file (JPG, PNG)")
        
        # Save uploaded file
        upload_dir = "uploads/images"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create unique filename
        file_ext = os.path.splitext(file.filename)[1] or ".jpg"
        filename = f"{uuid.uuid4()}{file_ext}"
        filepath = os.path.join(upload_dir, filename)
        
        # Save the file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"✅ Image saved: {filepath}")
        
        # Get CNN service
        cnn_service = req.app.state.cnn_service
        
        # Analyze image
        result = await cnn_service.analyze_image(filepath)
        
        print(f"✅ Analysis complete: {result['skin_type']}")
        
        return AnalysisResponse(
            skin_type=result["skin_type"],
            concerns=result["concerns"],
            acne_severity=result.get("acne_severity", "none"),
            pigmentation=result.get("pigmentation", "none"),
            confidence=result["confidence"],
            recommendations=result.get("recommendations", [
                "Use gentle cleanser twice daily",
                "Apply moisturizer suitable for your skin type",
                "Always use SPF 50 sunscreen",
                "Stay hydrated and maintain a healthy diet"
            ])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")