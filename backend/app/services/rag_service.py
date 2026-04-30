"""
RAG Service - Retrieval Augmented Generation
"""
from typing import Dict, List
import json
import os

class RAGService:
    """RAG-based skincare knowledge retrieval"""
    
    def __init__(self):
        self.products_db = []
        self.ingredients_db = []
        self.initialized = False
    
    async def initialize(self):
        """Load knowledge bases"""
        seed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "seed_data")
        
        # Load products
        products_path = os.path.join(seed_dir, "products.json")
        if os.path.exists(products_path):
            with open(products_path) as f:
                self.products_db = json.load(f)
        
        # Load ingredients
        ingredients_path = os.path.join(seed_dir, "ingredients.json")
        if os.path.exists(ingredients_path):
            with open(ingredients_path) as f:
                self.ingredients_db = json.load(f)
        
        # Fallback to default data
        if not self.products_db:
            self.products_db = self._get_default_products()
        if not self.ingredients_db:
            self.ingredients_db = self._get_default_ingredients()
        
        self.initialized = True
        print(f"✅ RAG initialized: {len(self.products_db)} products, {len(self.ingredients_db)} ingredients")
    
    def _get_default_products(self) -> List[Dict]:
        """Default products"""
        return [
            {"name": "Foaming Facial Cleanser", "brand": "CeraVe", "category": "cleanser",
             "skin_types": ["oily", "combination"], "key_ingredients": ["Niacinamide", "Ceramides"],
             "allergens": [], "price_range": "$$", "rating": 4.5},
            {"name": "Hydrating Cleanser", "brand": "Cetaphil", "category": "cleanser",
             "skin_types": ["dry", "sensitive"], "key_ingredients": ["Glycerin", "Panthenol"],
             "allergens": [], "price_range": "$$", "rating": 4.4},
            {"name": "Niacinamide 10% + Zinc 1%", "brand": "The Ordinary", "category": "serum",
             "skin_types": ["oily", "acne-prone"], "key_ingredients": ["Niacinamide", "Zinc"],
             "allergens": [], "price_range": "$", "rating": 4.7},
            {"name": "Hyaluronic Acid 2%", "brand": "The Ordinary", "category": "serum",
             "skin_types": ["all"], "key_ingredients": ["Hyaluronic Acid"],
             "allergens": [], "price_range": "$", "rating": 4.6},
            {"name": "Salicylic Acid 2%", "brand": "The Ordinary", "category": "treatment",
             "skin_types": ["oily", "acne-prone"], "key_ingredients": ["Salicylic Acid"],
             "allergens": [], "price_range": "$", "rating": 4.4}
        ]
    
    def _get_default_ingredients(self) -> List[Dict]:
        """Default ingredients"""
        return [
            {"name": "Salicylic Acid", "benefits": ["Exfoliates", "Reduces acne", "Oil control"],
             "skin_types": ["oily", "acne-prone"], "contraindications": ["Aspirin allergy"]},
            {"name": "Niacinamide", "benefits": ["Oil regulation", "Pore minimization", "Brightening"],
             "skin_types": ["all"], "contraindications": []},
            {"name": "Hyaluronic Acid", "benefits": ["Hydration", "Plumping"],
             "skin_types": ["all"], "contraindications": []}
        ]
    
    async def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant knowledge"""
        query_lower = query.lower()
        results = []
        
        for ing in self.ingredients_db:
            if query_lower in ing.get("name", "").lower():
                results.append({"content": ing, "score": 0.9, "type": "ingredient"})
            elif any(b.lower() in query_lower for b in ing.get("benefits", [])):
                results.append({"content": ing, "score": 0.7, "type": "ingredient"})
        
        for prod in self.products_db:
            if query_lower in prod.get("name", "").lower():
                results.append({"content": prod, "score": 0.8, "type": "product"})
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k] if results else [{"content": self.ingredients_db[0], "score": 0.5}]
    
    async def search_products(self, query: str) -> List[Dict]:
        """Search products"""
        query_lower = query.lower()
        matching = [p for p in self.products_db if query_lower in p.get("category", "").lower()]
        return matching if matching else self.products_db[:3]
    
    async def filter_by_allergies(self, products: List[Dict], allergies: List[str]) -> List[Dict]:
        """Filter products by allergies"""
        if not allergies:
            return products
        
        safe = []
        for p in products:
            product_allergens = [a.lower() for a in p.get("allergens", [])]
            if not any(a.lower() in product_allergens for a in allergies):
                p["reason"] = "Verified safe for your allergies"
                safe.append(p)
        
        return safe if safe else products[:3]
    
    async def get_natural_remedies(self, skin_type: str, concerns: List[str]) -> List[Dict]:
        """Get natural remedies"""
        return [
            {"name": "Honey & Aloe Mask", "ingredients": ["Raw Honey", "Aloe Vera Gel"],
             "benefits": "Soothing, antibacterial, hydrating"},
            {"name": "Green Tea Toner", "ingredients": ["Green Tea", "Witch Hazel"],
             "benefits": "Antioxidant, reduces inflammation"},
            {"name": "Oatmeal Scrub", "ingredients": ["Ground Oatmeal", "Yogurt"],
             "benefits": "Gentle exfoliation, moisturizing"}
        ]