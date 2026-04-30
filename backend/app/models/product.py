"""Product & Ingredient Models"""
from sqlalchemy import Column, Integer, String, Float, JSON, Boolean
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String)  # cleanser, moisturizer, serum, etc.
    skin_types = Column(JSON)  # ["oily", "combination"]
    key_ingredients = Column(JSON)  # ["Niacinamide", "Zinc"]
    allergens = Column(JSON)  # ["fragrance", "parabens"]
    price = Column(Float)
    rating = Column(Float)
    description = Column(String)
    usage = Column(String)

class Ingredient(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # active, humectant, emollient
    benefits = Column(JSON)  # ["hydrating", "anti-aging"]
    skin_types_suitable = Column(JSON)  # ["all", "oily"]
    comedogenic_rating = Column(Integer)  # 0-5
    safety_rating = Column(Integer)  # 1-10

class Allergen(Base):
    __tablename__ = "allergens"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    category = Column(String)  # fragrance, preservative, dye
    common_in = Column(JSON)  # ["perfumes", "lotions"]
    severity = Column(String)  # mild, moderate, severe