"""OCR Service - Extract text from reports"""
import os
import pytesseract

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRService:
    def __init__(self):
        pass
    
    async def extract_text(self, filepath: str) -> str:
        """Extract text from PDF or image"""
        ext = os.path.splitext(filepath)[1].lower()
        
        print(f"📄 Processing file: {filepath} (type: {ext})")
        
        if ext == '.pdf':
            return self._extract_pdf(filepath)
        elif ext == '.txt':
            return self._extract_txt(filepath)
        else:
            return self._extract_image(filepath)
    
    def _extract_pdf(self, filepath: str) -> str:
        """Extract from PDF"""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            print(f"✅ PDF text: {len(text)} chars")
            return text[:3000] if text.strip() else "No text found in PDF"
        except Exception as e:
            print(f"PDF error: {e}")
            return "Could not extract text from PDF"
    
    def _extract_image(self, filepath: str) -> str:
        """Extract from image using Tesseract OCR"""
        try:
            from PIL import Image
            img = Image.open(filepath)
            print(f"📷 Image size: {img.size}")
            
            # Use Tesseract to extract text
            text = pytesseract.image_to_string(img)
            
            print(f"✅ OCR extracted: {len(text)} chars")
            print(f"   Text preview: {text[:100]}...")
            
            return text[:3000] if text.strip() else "No text detected in image"
            
        except Exception as e:
            print(f"❌ OCR error: {e}")
            return "OCR failed. Is Tesseract installed?"
    
    def _extract_txt(self, filepath: str) -> str:
        """Read plain text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
                print(f"✅ Text file: {len(text)} chars")
                return text[:3000]
        except:
            return "Could not read text file"