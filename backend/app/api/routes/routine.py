"""Routine Generation API - AI-Powered"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()

class RoutineRequest(BaseModel):
    skin_type: str
    concerns: List[str] = []
    lifestyle: Optional[Dict] = {}
    routine_type: str = "both"

class RoutineResponse(BaseModel):
    morning: List[dict]
    night: List[dict]
    weekly: List[dict]
    explanation: str

@router.post("/generate", response_model=RoutineResponse)
async def generate_routine(request: RoutineRequest, req: Request):
    try:
        llm_service = req.app.state.llm_service
        
        routine = await llm_service.generate_routine(
            skin_type=request.skin_type,
            concerns=request.concerns or [],
            lifestyle=request.lifestyle or {},
            routine_type=request.routine_type
        )
        
        return RoutineResponse(
            morning=routine.get("morning", []),
            night=routine.get("night", []),
            weekly=routine.get("weekly", []),
            explanation=routine.get("explanation", "")
        )
    except Exception as e:
        print(f"Routine error: {e}")
        raise HTTPException(status_code=500, detail=str(e))