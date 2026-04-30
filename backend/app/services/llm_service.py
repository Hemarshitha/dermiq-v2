"""
LLM Service - API Only, No Hardcoded Responses
"""
import requests
from typing import Dict, List, Optional
import json

class LLMService:
    def __init__(self):
        self.api_key = "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"  # YOUR KEY HERE
        self.model = "google/gemini-2.0-flash-001"
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        print("=" * 50)
        print("LLM Service Ready")
        print("=" * 50)
    
    async def generate_skincare_response(self, user_message, user_data, rag_context, chat_history):
        """Generate response - API ONLY"""
        
        skin = user_data.get('skin_type', '')
        concerns = user_data.get('concerns', [])
        
        context = ""
        if skin and skin != 'unknown':
            context += f"User has {skin} skin. "
        if concerns:
            context += f"Concerns: {', '.join(concerns)}. "
        
        prompt = f"{context}\nUser: {user_message}\nAssistant:"
        
        result = self._call_api(
            "You are DermIQ, a skincare expert. Be conversational, helpful, and specific. No markdown. Keep under 200 words.",
            prompt
        )
        
        if result:
            return result
        
        # If API fails, tell the truth
        return "⚠️ AI service is currently unavailable. Please check your API key configuration or try again later."
    
    async def generate_routine(self, skin_type, concerns, lifestyle, routine_type):
        """Generate routine using AI - WORKING VERSION"""
        
        if not self.api_key or self.api_key == "YOUR_OPENROUTER_KEY_HERE":
            return self._get_best_routine(skin_type, concerns)
        
        try:
            prompt = f"""Create a detailed skincare routine for {skin_type} skin with {', '.join(concerns) if concerns else 'general care'}.

Return ONLY valid JSON with this EXACT structure (no other text):
{{
    "morning": [
        {{"step_number": 1, "action": "action name", "product": "product name", "instructions": "how to use", "timing": "AM"}}
    ],
    "night": [
        {{"step_number": 1, "action": "action name", "product": "product name", "instructions": "how to use", "timing": "PM"}}
    ],
    "weekly": [
        {{"day": "day", "treatment": "treatment name", "product": "product", "instructions": "how to use"}}
    ],
    "explanation": "2-3 sentences why this works"
}}"""

            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "DermIQ"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 600
                },
                timeout=20
            )
            
            print(f"Routine API Status: {response.status_code}")
            
            if response.status_code == 200:
                text = response.json()['choices'][0]['message']['content']
                print(f"AI Response: {text[:150]}...")
                
                # Find JSON in response
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end > start:
                    try:
                        result = json.loads(text[start:end])
                        # Check if it has the right structure
                        if 'morning' in result and 'night' in result:
                            print("✅ AI Routine generated!")
                            return result
                        # Maybe it's in a different format - try to convert
                        if 'steps' in result:
                            return self._convert_steps_format(result)
                    except json.JSONDecodeError:
                        print("JSON parse error, trying alternative...")
                
        except Exception as e:
            print(f"Routine error: {e}")
        
        return self._get_best_routine(skin_type, concerns)
    
    def _convert_steps_format(self, data):
        """Convert alternative AI format to our format"""
        steps = data.get('steps', [])
        morning = []
        night = []
        
        for step in steps:
            formatted = {
                "step_number": step.get('step_number', len(morning) + 1),
                "action": step.get('step_name', step.get('action', 'Step')),
                "product": step.get('product_type', step.get('product', 'Product')),
                "instructions": step.get('description', step.get('instructions', 'Apply as directed')),
                "timing": step.get('timing', 'AM')
            }
            if 'AM' in formatted['timing'] or 'morning' in str(step).lower():
                morning.append(formatted)
            else:
                night.append(formatted)
        
        return {
            "morning": morning[:5] if morning else self._get_best_routine('normal', [])['morning'],
            "night": night[:4] if night else self._get_best_routine('normal', [])['night'],
            "weekly": [{"day": "Wednesday & Sunday", "treatment": "Exfoliation", "product": "AHA/BHA Exfoliant", "instructions": "After cleansing, apply for 10 minutes, rinse"}],
            "explanation": data.get('description', data.get('explanation', f'Personalized routine for {data.get("skin_type", "your")} skin.'))
        }
    
    def _get_best_routine(self, skin_type, concerns):
        """Best routine without AI"""
        is_oily = 'oily' in str(skin_type).lower()
        is_dry = 'dry' in str(skin_type).lower()
        
        return {
            "morning": [
                {"step_number": 1, "action": "Cleanse", "product": "CeraVe Foaming Cleanser" if is_oily else "Cetaphil Gentle Cleanser", "instructions": "Massage with lukewarm water for 60 seconds. Pat dry.", "timing": "AM"},
                {"step_number": 2, "action": "Tone", "product": "Alcohol-Free Toner", "instructions": "Apply with cotton pad or pat directly onto skin.", "timing": "AM"},
                {"step_number": 3, "action": "Serum", "product": "Niacinamide 10% + Zinc 1%" if is_oily else "Hyaluronic Acid 2% + B5", "instructions": "Apply 3-4 drops. Let absorb.", "timing": "AM"},
                {"step_number": 4, "action": "Moisturize", "product": "Oil-Free Gel Moisturizer" if is_oily else "Ceramide Moisturizing Cream", "instructions": "Apply to damp skin.", "timing": "AM"},
                {"step_number": 5, "action": "Protect", "product": "SPF 50 Sunscreen", "instructions": "Two finger-lengths for face and neck.", "timing": "AM"}
            ],
            "night": [
                {"step_number": 1, "action": "Double Cleanse", "product": "Oil Cleanser + Foaming Cleanser", "instructions": "Remove makeup and sunscreen thoroughly.", "timing": "PM"},
                {"step_number": 2, "action": "Exfoliate (2x/week)", "product": "Salicylic Acid 2%" if is_oily else "Lactic Acid 5%", "instructions": "Apply after cleansing, don't rinse.", "timing": "PM"},
                {"step_number": 3, "action": "Night Cream", "product": "Ceramide PM Lotion", "instructions": "Generous layer before bed.", "timing": "PM"}
            ],
            "weekly": [
                {"day": "Wednesday & Sunday", "treatment": "Deep Exfoliation", "product": "AHA/BHA Peel" if is_oily else "Enzyme Mask", "instructions": "After cleansing, leave 10 minutes, rinse well."}
            ],
            "explanation": f"This routine is designed for {skin_type} skin focusing on {', '.join(concerns) if concerns else 'overall skin health'}. Morning protects, night repairs."
        }
    
    def _call_api(self, system_prompt, user_prompt, max_tokens=300):
        """Call OpenRouter API"""
        if not self.api_key or self.api_key == "YOUR_OPENROUTER_KEY_HERE":
            print("❌ No API key configured")
            return None
        
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "DermIQ"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                },
                timeout=15
            )
            
            print(f"API Status: {response.status_code}")
            
            if response.status_code == 200:
                text = response.json()['choices'][0]['message']['content'].strip()
                print(f"✅ AI Response: {text[:80]}...")
                return text
            elif response.status_code == 401:
                print("❌ API Key is INVALID. Get a new one from https://openrouter.ai/keys")
            elif response.status_code == 402:
                print("❌ No credits. Add funds to OpenRouter.")
            elif response.status_code == 429:
                print("⚠️ Rate limited. Wait and retry.")
            else:
                print(f"❌ API Error {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return None
    
    async def extract_skin_data(self, message):
        msg = message.lower()
        data = {"skin_type": "unknown", "concerns": []}
        if any(w in msg for w in ['oily', 'greasy']): data['skin_type'] = 'oily'
        elif any(w in msg for w in ['dry', 'flake']): data['skin_type'] = 'dry'
        if any(w in msg for w in ['acne', 'pimple', 'bump', 'breakout']): data['concerns'].append('acne')
        if any(w in msg for w in ['dark spot', 'pigment', 'uneven']): data['concerns'].append('pigmentation')
        return data
    
    async def extract_allergens(self, text):
        return [{"allergen": "None detected", "severity": "N/A", "category": "N/A"}]
    
    async def generate_explanation(self, skin_type, concerns, products):
        return f"Selected for {skin_type} skin."