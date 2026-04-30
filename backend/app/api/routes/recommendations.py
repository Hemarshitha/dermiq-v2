"""Recommendations API - AI-Powered"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
import json

router = APIRouter()

class RecommendationRequest(BaseModel):
    skin_type: str
    concerns: List[str] = []
    allergies: Optional[List[str]] = []
    preferences: Optional[Dict] = {}

class RecommendationResponse(BaseModel):
    products: List[Dict]
    natural_remedies: List[Dict]
    explanation: str
    safety_summary: str

@router.post("/get-recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest, req: Request):
    try:
        llm_service = req.app.state.llm_service
        rag_service = req.app.state.rag_service
        
        # Get products from RAG
        query = f"{request.skin_type} {', '.join(request.concerns)}"
        products = await rag_service.search_products(query)
        safe_products = await rag_service.filter_by_allergies(products, request.allergies or [])
        natural_remedies = await rag_service.get_natural_remedies(request.skin_type, request.concerns or [])
        
        # Get AI explanation
        explanation = await llm_service.generate_explanation(
            request.skin_type,
            request.concerns or [],
            safe_products[:3]
        )
        
        return RecommendationResponse(
            products=[{
                "name": p.get("name", ""),
                "brand": p.get("brand", "N/A"),
                "category": p.get("category", ""),
                "reason": p.get("reason", "Recommended for your skin type"),
                "safety_check": True,
                "price_range": p.get("price_range", "$$")
            } for p in safe_products[:5]],
            natural_remedies=natural_remedies[:3],
            explanation=explanation,
            safety_summary="All recommended products verified safe for your allergies."
        )
    except Exception as e:
        print(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))