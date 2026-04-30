"""Application Configuration"""
import os
from dotenv import load_dotenv

# Load .env file BEFORE anything else
load_dotenv()

class Settings:
    """Application settings"""
    
    def __init__(self):
        # App
        self.APP_NAME = "DermIQ"
        self.APP_VERSION = "2.0.0"
        self.DEBUG = True
        
        # Server
        self.HOST = "0.0.0.0"
        self.PORT = 8000
        
        # Database
        self.DATABASE_URL = "sqlite:///./dermiq.db"
        
        # API Keys - Read directly from environment
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
        self.PINECONE_ENV = "us-west1-gcp"
        
        # Upload
        self.UPLOAD_DIR = "uploads"
        self.MAX_UPLOAD_SIZE = 10 * 1024 * 1024
        
        # Model Paths
        self.CNN_MODEL_PATH = "ml/models/skin_model.h5"
        
        # Create upload directory
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        
        # Print key status
        if self.GEMINI_API_KEY and self.GEMINI_API_KEY != "your-gemini-api-key-here":
            print(f"✅ API Key loaded: {self.GEMINI_API_KEY[:10]}...")
        else:
            print("❌ No API Key found in .env file")

# Create settings instance
settings = Settings()