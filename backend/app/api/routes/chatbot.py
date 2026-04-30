"""Chatbot API - Context-Aware"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Dict

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_profile: Optional[Dict] = None

class ChatResponse(BaseModel):
    response: str
    extracted_data: Optional[Dict] = None
    session_id: str

sessions = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    try:
        llm_service = req.app.state.llm_service
        
        session_id = request.session_id or "default"
        if session_id not in sessions:
            sessions[session_id] = {
                "skin_type": None,
                "concerns": [],
                "last_topic": None,
                "history": []
            }
        
        session = sessions[session_id]
        msg = request.message
        
        # Track what user is talking about
        msg_lower = msg.lower()
        
        # Update skin type if mentioned
        if 'oily' in msg_lower:
            session['skin_type'] = 'oily'
        elif 'dry' in msg_lower:
            session['skin_type'] = 'dry'
        elif 'combination' in msg_lower:
            session['skin_type'] = 'combination'
        
        # Update concerns
        for concern in ['acne', 'pimple', 'bump', 'breakout']:
            if concern in msg_lower and 'acne' not in session['concerns']:
                session['concerns'].append('acne')
                break
        
        # Track last topic
        if 'product' in msg_lower or 'ordinary' in msg_lower:
            session['last_topic'] = 'product_reaction'
        elif 'routine' in msg_lower:
            session['last_topic'] = 'routine'
        elif 'bump' in msg_lower or 'acne' in msg_lower:
            session['last_topic'] = 'acne'
        
        # Build user data with full context
        user_data = {
            "skin_type": session['skin_type'] or "unknown",
            "concerns": session['concerns'] or ["general"],
            "last_topic": session.get('last_topic', '')
        }
        
        # Get response from LLM
        response = await llm_service.generate_skincare_response(
            msg,
            user_data,
            [],
            session['history'][-5:]
        )
        
        # Store in history
        session['history'].append({"role": "user", "content": msg})
        session['history'].append({"role": "assistant", "content": response})
        
        print(f"💬 {msg[:40]} → {response[:40]}")
        
        return ChatResponse(
            response=response,
            extracted_data={"skin_type": session['skin_type'], "concerns": session['concerns']},
            session_id=session_id
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))