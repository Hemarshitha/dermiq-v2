"""Analysis & Recommendation Models"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SkinAnalysis(Base):
    __tablename__ = "skin_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)
    skin_type = Column(String)
    concerns = Column(JSON)
    acne_severity = Column(String)
    pigmentation_level = Column(String)
    confidence_score = Column(Float)
    recommendations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="analyses")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    analysis_id = Column(Integer, ForeignKey("skin_analyses.id"))
    products = Column(JSON)  # List of recommended products
    natural_remedies = Column(JSON)  # Traditional remedies
    explanation = Column(String)  # AI explanation
    safety_checked = Column(JSON)  # Allergen verification
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="recommendations")

class SkincareRoutine(Base):
    __tablename__ = "skincare_routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"))
    morning_steps = Column(JSON)
    night_steps = Column(JSON)
    weekly_steps = Column(JSON)
    ai_explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)