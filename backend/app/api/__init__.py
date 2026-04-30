from app.api.routes.chatbot import router as chatbot_router
from app.api.routes.analysis import router as analysis_router
from app.api.routes.ocr import router as ocr_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.routine import router as routine_router

__all__ = [
    "chatbot_router",
    "analysis_router",
    "ocr_router",
    "recommendations_router",
    "routine_router"
]