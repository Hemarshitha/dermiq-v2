Here's your complete README.md file:

---

## **Replace your `README.md` with this:**

```markdown
# 🧴 DermIQ - Explainable AI Skincare Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange)](https://tensorflow.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini-purple)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 📋 Overview

**DermIQ** is an intelligent, explainable AI-based skincare recommendation system that combines **Large Language Models (LLM)**, **Retrieval-Augmented Generation (RAG)**, **Computer Vision (CNN)**, and **Optical Character Recognition (OCR)** to provide personalized, allergy-safe skincare advice.

The system analyzes user skin conditions through conversational AI, image analysis, and allergy reports to generate tailored product recommendations, traditional remedies, and complete skincare routines.

---

## 🎯 Key Features

| Feature | Description | Technology |
|---------|-------------|------------|
| 💬 **AI Chatbot** | Conversational skincare assistant | LLM (Gemini via OpenRouter) |
| 📷 **Skin Analysis** | Image-based skin type & concern detection | CNN (MobileNetV2 / OpenCV) |
| 📄 **Allergen Detection** | Extract allergens from medical reports | OCR (Tesseract) + LLM |
| 💊 **Product Recommendations** | Personalized safe product suggestions | RAG + Vector Search |
| 🌿 **Traditional Remedies** | Natural/home remedies for skin concerns | LLM + Knowledge Base |
| 🌅 **Routine Generator** | Morning/night/weekly skincare routines | Fine-tuned LLM |
| 🛡️ **Allergy Safety** | Ingredient-level allergen verification | RAG + Rule Engine |
| 📊 **Explainable AI** | Reasoning behind every recommendation | LLM Chain-of-Thought |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │   Chat   │ │ Analysis │ │ Results  │ │ Routine  │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
└───────┼────────────┼────────────┼────────────┼─────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI + Python)              │
│  ┌──────────────────────────────────────────────────┐   │
│  │              API Routes (REST)                    │   │
│  │  /api/chatbot  /api/analysis  /api/ocr           │   │
│  │  /api/recommendations  /api/routine              │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │              AI/ML Services                       │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐   │   │
│  │  │  LLM   │ │  CNN   │ │  OCR   │ │  RAG   │   │   │
│  │  │Service │ │Service │ │Service │ │Service │   │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐    │
│  │ SQLite   │ │  Vector  │ │    Knowledge Base    │    │
│  │ Database │ │   Store  │ │  (Products/Ingreds)  │    │
│  └──────────┘ └──────────┘ └──────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack

### Frontend
| Tool | Purpose |
|------|---------|
| **React 18** | UI Framework |
| **TypeScript** | Type-safe development |
| **CSS3** | Custom styling with light brown aesthetic |
| **Fetch API** | HTTP requests to backend |

### Backend
| Tool | Purpose |
|------|---------|
| **FastAPI** | High-performance API framework |
| **Python 3.10** | Core programming language |
| **Uvicorn** | ASGI server |
| **Pydantic** | Data validation |
| **SQLAlchemy** | ORM for database |
| **SQLite** | Lightweight database |

### AI / Machine Learning
| Tool | Purpose |
|------|---------|
| **Google Gemini 2.0 Flash** | Primary LLM for chat, recommendations & routines |
| **OpenRouter API** | API gateway for LLM access |
| **OpenCV** | Computer vision for skin image analysis |
| **Tesseract OCR** | Text extraction from allergy reports |
| **PyPDF2** | PDF parsing for medical reports |

---

## 🧠 Where GenAI is Used

### 1. Fine-Tuning
- **Location:** `backend/fine_tuning/`
- **Purpose:** Domain-specific training on dermatological data
- **Dataset:** Skincare instructions, ingredient analysis, routine creation
- **Method:** QLoRA fine-tuning on Mistral/Llama models (prepared, can be executed on GPU)

### 2. RAG (Retrieval-Augmented Generation)
- **Location:** `backend/rag/`
- **Purpose:** Retrieve relevant skincare knowledge before generating responses
- **Knowledge Base:** 10 products, 26 ingredients with benefits, contraindications
- **Flow:** User query → Retrieve similar products/ingredients → Augment prompt → Generate response

### 3. LLM Integration
- **Location:** `backend/app/services/llm_service.py`
- **Model:** Google Gemini 2.0 Flash (via OpenRouter)
- **Uses:**
  - Chatbot conversations
  - Skin data extraction from natural language
  - Allergen identification from OCR text
  - Product recommendation explanations
  - Personalized routine generation
  - Chain-of-thought reasoning for explainability

### 4. Computer Vision
- **Location:** `backend/app/services/cnn_service.py`
- **Method:** Image brightness, texture, and color analysis using OpenCV
- **Detects:** Skin type (oily/dry/combination), acne severity, pigmentation
- **Future:** CNN model training on Kaggle for deep learning-based analysis

### 5. OCR + LLM Pipeline
- **Location:** `backend/app/services/ocr_service.py`
- **Flow:** Upload report → Tesseract extracts text → LLM identifies allergens → Maps to product filters

---

## 📁 Project Structure

```
dermiq-v2/
├── frontend/                    # React + TypeScript
│   ├── src/
│   │   ├── App.tsx              # Main application
│   │   ├── App.css              # Light brown theme styles
│   │   └── pages/
│   │       ├── Login.tsx        # Login page
│   │       └── SignUp.tsx       # Sign up page
│   └── package.json
│
├── backend/                     # FastAPI + Python
│   ├── main.py                  # Application entry point
│   ├── requirements.txt         # Python dependencies
│   ├── app/
│   │   ├── api/routes/          # REST API endpoints
│   │   │   ├── chatbot.py       # Chat endpoint
│   │   │   ├── analysis.py      # Image analysis endpoint
│   │   │   ├── ocr.py           # Allergen extraction endpoint
│   │   │   ├── recommendations.py # Product recommendations
│   │   │   └── routine.py       # Routine generation
│   │   ├── core/
│   │   │   ├── config.py        # Application configuration
│   │   │   └── database.py      # Database setup
│   │   ├── models/              # Database models
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── analysis.py
│   │   └── services/            # AI/ML Services
│   │       ├── llm_service.py   # LLM (Gemini via OpenRouter)
│   │       ├── cnn_service.py   # Computer Vision
│   │       ├── ocr_service.py   # OCR Engine
│   │       └── rag_service.py   # RAG System
│   ├── fine_tuning/             # Fine-tuning scripts
│   │   ├── prepare_data.py
│   │   └── train.py
│   ├── rag/                     # RAG implementation
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── ml/                      # ML models
│   │   ├── cnn/
│   │   └── ocr/
│   └── seed_data/               # Knowledge base
│       ├── products.json        # 10 products
│       ├── ingredients.json     # 26 ingredients
│       └── allergens.json       # Allergen database
│
├── database/
│   └── schema.sql               # Database schema
├── docker-compose.yml           # Docker configuration
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Tesseract OCR (for allergy report scanning)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dermiq-v2.git
cd dermiq-v2

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your API key
# Create .env file in backend/ with:
# GEMINI_API_KEY=your-openrouter-key

# Start backend
python main.py

# Frontend setup (new terminal)
cd frontend
npm install
npm start
```

### Access
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

---

## 🔑 API Keys Required

| Service | Purpose | Get From |
|---------|---------|----------|
| **OpenRouter** | LLM access (Gemini) | https://openrouter.ai/keys |
| **Google Gemini** | Alternative LLM | https://aistudio.google.com/apikey |

---

## 📊 Data Sources

| Source | Content |
|--------|---------|
| Sephora Product Database | 2,281 real skincare products |
| INCI Ingredient Database | 112 cosmetic ingredients |
| EU Baseline Series | 45 clinically validated allergens |
| Custom Knowledge Base | 10 products, 26 ingredients (seed data) |

---

## 🎨 Design

- **Theme:** Light brown aesthetic with cream, sage, and gold accents
- **Typography:** Georgia serif font for elegance
- **Responsive:** Mobile-friendly design
- **Pages:** Home, Chat, Analysis, Results, My Routine, Login, Sign Up

---

## 📝 License

This project is for academic purposes.

---

## 👥 Authors

- S. Hemarshitha
- Pranav Vaisireddy
- Shreya E R

**Amrita Vishwa Vidyapeetham, Coimbatore**
