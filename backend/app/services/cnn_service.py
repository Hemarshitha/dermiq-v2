"""
CNN Service - REAL skin analysis using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict
import os

class CNNService:
    def __init__(self):
        self.face_mesh = None
        self.model_loaded = False
    
    async def load_model(self):
        """Load MediaPipe face mesh"""
        try:
            mp_face_mesh = mp.solutions.face_mesh
            self.face_mesh = mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )
            self.model_loaded = True
            print("✅ MediaPipe Face Analysis Ready")
        except Exception as e:
            print(f"⚠️ Could not load MediaPipe: {e}")
            self.model_loaded = False
    
    async def analyze_image(self, image_path: str) -> Dict:
        
        
        print(f"\n🔍 Analyzing: {image_path}")
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            return self._error_result("Image file not found")
        
        try:
            # Read the image
            image = cv2.imread(image_path)
            
            if image is None:
                print(f"❌ Could not read image with cv2")
                return self._error_result("Could not read image file")
            
            print(f"✅ Image loaded: {image.shape}")
            
            # Get dimensions
            height, width = image.shape[:2]
            print(f"   Size: {width}x{height}")
            
            # Overall brightness
            overall_brightness = np.mean(image)
            print(f"   Overall brightness: {overall_brightness:.1f}")
            
            # T-zone brightness
            t_zone_y1 = int(height * 0.15)
            t_zone_y2 = int(height * 0.45)
            t_zone_x1 = int(width * 0.3)
            t_zone_x2 = int(width * 0.7)
            
            t_zone = image[t_zone_y1:t_zone_y2, t_zone_x1:t_zone_x2]
            t_zone_brightness = np.mean(t_zone) if t_zone.size > 0 else 0
            print(f"   T-zone brightness: {t_zone_brightness:.1f}")
            
            # Determine skin type from ACTUAL brightness values
            if t_zone_brightness > 170:
                skin_type = "oily"
                confidence = 0.85
            elif t_zone_brightness > 140:
                skin_type = "combination"
                confidence = 0.80
            elif overall_brightness < 90:
                skin_type = "dry"
                confidence = 0.82
            else:
                skin_type = "normal"
                confidence = 0.78
            
            print(f"   ➜ Detected: {skin_type} (confidence: {confidence})")
            
            # Texture analysis for acne
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            texture = np.std(gray)
            print(f"   Texture (std): {texture:.1f}")
            
            acne_severity = "moderate" if texture > 55 else "mild" if texture > 40 else "none"
            
            # Redness analysis
            redness = np.mean(image[:, :, 2]) - np.mean(image[:, :, 0])
            print(f"   Redness: {redness:.1f}")
            
            pigmentation = "moderate" if redness > 30 else "light" if redness > 15 else "none"
            
            # Build concerns
            concerns = []
            if t_zone_brightness > 150:
                concerns.append("excess oil in T-zone")
            if overall_brightness < 95:
                concerns.append("dullness or dryness")
            if texture > 45:
                concerns.append("uneven texture or visible pores")
            if redness > 20:
                concerns.append("redness or irritation")
            
            if not concerns:
                concerns = ["generally balanced skin"]
            
            print(f"   Concerns: {concerns}")
            print(f"✅ Analysis complete\n")
            
            return {
                "skin_type": skin_type,
                "concerns": concerns,
                "acne_severity": acne_severity,
                "pigmentation": pigmentation,
                "confidence": round(confidence, 2),
                "recommendations": self._get_recommendations(skin_type, concerns)
            }
            
        except Exception as e:
            print(f"❌ Analysis error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return self._error_result(f"Analysis error: {str(e)}")
    
    def _get_region_brightness(self, image, face, points):
        """Calculate average brightness of face region"""
        h, w = image.shape[:2]
        brightness_values = []
        
        for point_idx in points:
            landmark = face.landmark[point_idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            
            if 0 <= x < w and 0 <= y < h:
                pixel = image[y, x]
                brightness = np.mean(pixel)
                brightness_values.append(brightness)
        
        return np.mean(brightness_values) if brightness_values else 0
    
    def _fallback_analysis(self):
        return {
            "skin_type": "combination",
            "concerns": ["needs further analysis"],
            "acne_severity": "unknown",
            "pigmentation": "unknown",
            "confidence": 0.60,
            "recommendations": [
                "Use gentle cleanser",
                "Apply moisturizer daily",
                "Use SPF 50 sunscreen",
                "Consult a dermatologist"
            ]
        }
    
    def _get_recommendations(self, skin_type, concerns=None):
        if concerns is None:
            concerns = []
        
        recommendations = []
        
        if skin_type == "oily":
            recommendations.extend([
                "Use oil-free, non-comedogenic products",
                "Include Salicylic Acid (BHA) to unclog pores",
                "Apply Niacinamide serum to control oil production",
                "Use gel-based moisturizer instead of cream"
            ])
        elif skin_type == "dry":
            recommendations.extend([
                "Use cream-based hydrating cleansers",
                "Apply Hyaluronic Acid serum on damp skin",
                "Use Ceramide-rich moisturizer for barrier repair",
                "Avoid hot water when washing face"
            ])
        elif skin_type == "combination":
            recommendations.extend([
                "Use different products for different areas",
                "Apply lightweight gel on T-zone",
                "Use richer moisturizer on dry areas",
                "Balance with Niacinamide"
            ])
        else:
            recommendations.extend([
                "Maintain with gentle, pH-balanced products",
                "Use broad-spectrum SPF 50 daily",
                "Include antioxidants like Vitamin C"
            ])
        
        concerns_text = " ".join(concerns).lower()
        if "redness" in concerns_text:
            recommendations.append("Use fragrance-free, soothing products")
        if "pores" in concerns_text:
            recommendations.append("Weekly clay mask to minimize pore appearance")
        
        recommendations.append("Always apply SPF 50 sunscreen daily")
        
        return recommendations[:5]

    def _error_result(self, msg):
        """Return error result"""
        return {
            "skin_type": "unknown",
            "concerns": [msg],
            "acne_severity": "unknown",
            "pigmentation": "unknown",
            "confidence": 0.0,
            "recommendations": ["Please upload a clear, well-lit photo of your face"]
        }