"""OCR API - Extract allergens using LLM"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
import os
import uuid
import shutil
import requests
import json

router = APIRouter()

class AllergenItem(BaseModel):
    allergen: str
    severity: str
    category: str

class OCRExtractionResponse(BaseModel):
    allergens_found: List[AllergenItem]
    raw_text: str
    confidence: float

@router.post("/extract-allergens", response_model=OCRExtractionResponse)
async def extract_allergens(
    file: UploadFile = File(...),
    req: Request = None
):
    """Extract allergens from reports using OCR + LLM"""
    try:
        # Validate file
        allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Upload PDF or image files only")
        
        # Save file
        upload_dir = "uploads/reports"
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"✅ Report saved: {filepath}")
        
        # Get OCR service
        ocr_service = req.app.state.ocr_service
        extracted_text = await ocr_service.extract_text(filepath)
        
        print(f"📄 Extracted {len(extracted_text)} chars")
        
        # Use LLM to analyze the text
        llm_service = req.app.state.llm_service
        
        # Direct LLM call for allergen extraction
        allergens = await _extract_allergens_with_llm(extracted_text, llm_service)
        
        print(f"🔍 Found {len(allergens)} allergens")
        
        return OCRExtractionResponse(
            allergens_found=[
                AllergenItem(
                    allergen=a.get('allergen', 'Unknown'),
                    severity=a.get('severity', 'N/A'),
                    category=a.get('category', 'N/A')
                ) for a in allergens
            ],
            raw_text=extracted_text[:500],
            confidence=0.90
        )
        
    except Exception as e:
        print(f"❌ OCR error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


async def _extract_allergens_with_llm(text: str, llm_service) -> List[Dict]:
    """Use LLM to intelligently extract allergens"""
    
    # Get API details from llm_service
    api_key = getattr(llm_service, 'api_key', None)
    model = getattr(llm_service, 'model', 'google/gemini-2.0-flash-001')
    
    if api_key and api_key != "YOUR_OPENROUTER_KEY_HERE":
        try:
            prompt = """You are a medical report analyzer. Extract ALL allergens with positive reactions from this allergy test report.

Report Text:
{text}

Instructions:
1. Only extract allergens that show POSITIVE or ALLERGIC reactions
2. Do NOT include negative results
3. Determine severity from the report (mild, moderate, severe, high)
4. Categorize each allergen (fragrance, preservative, metal, natural, etc.)

Return ONLY a valid JSON array. No other text:
[
    {{"allergen": "Exact Name from Report", "severity": "moderate", "category": "fragrance"}}
]

If NO positive allergens found, return: [{{"allergen": "No positive reactions found", "severity": "N/A", "category": "N/A"}}]""".format(text=text[:3000])
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer " + api_key,
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "DermIQ"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 500
                },
                timeout=20
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                print(f"LLM Response: {content[:300]}")
                
                # Extract JSON
                start = content.find('[')
                end = content.rfind(']') + 1
                if start != -1 and end > start:
                    try:
                        result = json.loads(content[start:end])
                        return result
                    except:
                        pass
                return [{"allergen": "Could not parse results", "severity": "N/A", "category": "N/A"}]
            else:
                print(f"LLM API error: {response.status_code}")
                
        except Exception as e:
            print(f"LLM call error: {e}")
    
    # Fallback: Simple keyword check for common allergens
    return _simple_allergen_check(text)


def _simple_allergen_check(text: str) -> List[Dict]:
    """Simple fallback - only detects exact allergen names from standard reports"""
    text_lower = text.lower()
    found = []
    
    # Only check for exact allergen names that appear in standard allergy reports
    # Look for lines with "positive" or "+" indicators
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        # Check if line indicates a positive reaction
        is_positive = any(word in line_lower for word in ['positive', 'reaction', 'observed', '+', 'hypersensitivity'])
        
        if is_positive:
            # Extract allergen name from the line
            for allergen_name in ['fragrance mix', 'formaldehyde', 'benzyl alcohol', 
                                  'lanolin', 'paraben', 'nickel', 'sulfate', 'latex',
                                  'balsam of peru', 'quaternium', 'imidazolidinyl',
                                  'dmdm hydantoin', 'methylisothiazolinone',
                                  'cocamidopropyl betaine', 'propylene glycol']:
                if allergen_name in line_lower:
                    found.append({
                        "allergen": allergen_name.title(),
                        "severity": "moderate",
                        "category": "reported allergen"
                    })
    
    if found:
        return found
    
    return [{"allergen": "Upload clear allergy report for detection", "severity": "N/A", "category": "N/A"}]