"""User Models"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    skin_profile = relationship("SkinProfile", back_populates="user", uselist=False)
    analyses = relationship("SkinAnalysis", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class SkinProfile(Base):
    __tablename__ = "skin_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skin_type = Column(String)  # oily, dry, combination, normal
    concerns = Column(JSON)  # ["acne", "pigmentation", "aging"]
    sensitivities = Column(JSON)  # ["fragrance", "alcohol"]
    allergies = Column(JSON)  # ["lanolin", "parabens"]
    
    user = relationship("User", back_populates="skin_profile")