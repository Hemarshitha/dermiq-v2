"""
DermIQ - Main Backend Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import time
from loguru import logger

from app.api.routes import (
    chatbot_router,
    analysis_router,
    recommendations_router,
    routine_router,
    ocr_router
)

from app.services.llm_service import LLMService
from app.services.cnn_service import CNNService
from app.services.ocr_service import OCRService
from app.services.rag_service import RAGService

logger.add("logs/dermiq.log", rotation="100 MB", retention="7 days")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting DermIQ Backend...")
    
    app.state.llm_service = LLMService()
    app.state.cnn_service = CNNService()
    app.state.ocr_service = OCRService()
    app.state.rag_service = RAGService()
    
    await app.state.rag_service.initialize()
    await app.state.cnn_service.load_model()
    
    logger.info("All services initialized")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="DermIQ API",
    version="2.0.0",
    description="AI-Powered Skincare Recommendation System",
    lifespan=lifespan
)

# CORS - Allow ALL origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Handle OPTIONS requests for CORS
    if request.method == "OPTIONS":
        response = JSONResponse(content={"message": "OK"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    return response

# Include routers
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(ocr_router, prefix="/api/ocr", tags=["OCR"])
app.include_router(recommendations_router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(routine_router, prefix="/api/routine", tags=["Routine"])

@app.get("/")
async def root():
    return {
        "name": "DermIQ API",
        "version": "2.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "llm": "available",
            "cnn": "simulation" if not CNNService().model_loaded else "loaded",
            "ocr": "available",
            "rag": "available"
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)