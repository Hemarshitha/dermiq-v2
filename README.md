# 🧴 DermIQ - Explainable AI Skincare Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange)](https://tensorflow.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini-purple)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Overview

**DermIQ** is an intelligent, explainable AI-based skincare recommendation system that integrates:

* Large Language Models (LLM)
* Retrieval-Augmented Generation (RAG)
* Computer Vision (CNN)
* Optical Character Recognition (OCR)

to provide **personalized, allergy-safe skincare recommendations**.

It analyzes:

* User conversations
* Skin images
* Medical/allergy reports

to generate:

* Product recommendations
* Traditional remedies
* Complete skincare routines

---

## 🎯 Key Features

| Feature                    | Description                       | Technology   |
| -------------------------- | --------------------------------- | ------------ |
| 💬 AI Chatbot              | Conversational skincare assistant | Gemini (LLM) |
| 📷 Skin Analysis           | Detects skin type & issues        | OpenCV / CNN |
| 📄 Allergen Detection      | Extracts allergens from reports   | OCR + LLM    |
| 💊 Product Recommendations | Personalized safe products        | RAG          |
| 🌿 Traditional Remedies    | Natural skincare suggestions      | LLM          |
| 🌅 Routine Generator       | Daily skincare plans              | LLM          |
| 🛡️ Allergy Safety         | Ingredient-level filtering        | RAG + Rules  |
| 📊 Explainable AI          | Reasoning behind outputs          | LLM          |

---

## 🏗️ Architecture

```
Frontend (React + TypeScript)
        ↓
Backend (FastAPI)
        ↓
AI Services (LLM + CNN + OCR + RAG)
        ↓
Database (SQLite + Vector Store + Knowledge Base)
```

---

## 🔧 Technology Stack

### Frontend

* React 18
* TypeScript
* CSS3
* Fetch API

### Backend

* FastAPI
* Python 3.10
* Uvicorn
* Pydantic
* SQLAlchemy
* SQLite

### AI / ML

* Google Gemini 2.0 Flash (via OpenRouter)
* OpenCV
* Tesseract OCR
* PyPDF2

---

## 🧠 Where GenAI is Used

### 1. Fine-Tuning

* **Location:** `backend/fine_tuning/`
* Domain-specific dermatology dataset
* QLoRA fine-tuning (Mistral/Llama models)

---

### 2. RAG (Retrieval-Augmented Generation)

* **Location:** `backend/rag/`
* Knowledge base:

  * 10 products
  * 26 ingredients
* Flow:

  ```
  Query → Retrieval → Augmentation → Generation
  ```

---

### 3. LLM Integration

* **Location:** `backend/app/services/llm_service.py`
* Uses:

  * Chatbot
  * Recommendations
  * Routine generation
  * Allergen extraction
  * Explainability

---

### 4. Computer Vision

* **Location:** `backend/app/services/cnn_service.py`
* Detects:

  * Skin type
  * Acne
  * Pigmentation

---

### 5. OCR + LLM Pipeline

* **Location:** `backend/app/services/ocr_service.py`
* Flow:

  ```
  Upload → OCR → LLM → Allergen Mapping
  ```

---

## 📁 Project Structure

```
dermiq-v2/
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── pages/
│   │       ├── Login.tsx
│   │       └── SignUp.tsx
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│
├── database/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* Node.js 18+
* Tesseract OCR

---

### Installation

```bash
git clone https://github.com/yourusername/dermiq-v2.git
cd dermiq-v2
```

---

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

---

## 🌐 Access

* Frontend: http://localhost:3000
* Backend: http://localhost:8000
* API Docs: http://localhost:8000/docs

---

## 🔑 API Keys Required

| Service       | Purpose       |
| ------------- | ------------- |
| OpenRouter    | Gemini access |
| Google Gemini | LLM           |

---

## 📊 Data Sources

* Sephora dataset
* INCI ingredient database
* EU allergen dataset
* Custom dataset

---

## 🎨 Design

* Light brown aesthetic
* Clean UI
* Mobile responsive

---

## 👥 Authors

* S. Hemarshitha
* Pranav Vaisireddy
* Shreya E R

**Amrita Vishwa Vidyapeetham, Coimbatore**

---

## 📝 License

MIT License (Academic Use)
