# 🧠 ResuMind AI

AI-powered Resume & Document Intelligence Platform

**Python | FastAPI | Streamlit | Qdrant | Ollama | spaCy**

Analyze resumes · Extract insights · Chat with documents · Match jobs · All locally

---

## 🚀 Live Demo

👉 Frontend: https://resumind-ai-cda69uig7pmz4vcnluckrw.streamlit.app

⚠️ Backend runs locally (due to local LLM + vector DB)

---

## 📸 Screenshots

### 🏠 Home Page

### 📊 Resume Dashboard

### 💬 AI Chat with Citations

### 🎯 Job Match Analyzer

### 🧠 Blackbox AI Assistant

---

## 🚀 Features

| Feature                  | Description                             |
| ------------------------ | --------------------------------------- |
| 📄 Resume Parsing        | Extracts name, email, skills, education |
| 📊 Resume Score          | AI-based scoring (0–100)                |
| 🤖 AI Feedback           | Recruiter-style suggestions             |
| 🔍 Semantic Search       | RAG + Qdrant                            |
| 💬 Chat with Resume      | Answers with citations                  |
| 🎯 Job Matching          | Skill comparison                        |
| 🧠 Blackbox AI           | General AI assistant                    |
| 📚 Document Intelligence | Extract structured data                 |

---

## 🛠 Tech Stack

| Layer      | Tech                 |
| ---------- | -------------------- |
| Backend    | FastAPI              |
| Frontend   | Streamlit            |
| Vector DB  | Qdrant               |
| Embeddings | SentenceTransformers |
| LLM        | Ollama (phi3)        |
| NLP        | spaCy                |

---

## ▶️ Run Locally

### 1. Start Qdrant

docker run -p 6333:6333 qdrant/qdrant

### 2. Start Backend

cd backend
python -m uvicorn main:app --reload

### 3. Start Frontend

cd backend
streamlit run app_ui.py

---

## ⚠️ Important Note

Full AI features require:

* Ollama installed
* phi3 model running

---

## ✅ Project Status

* Frontend deployed ✅
* Backend local ✅
* RAG pipeline working ✅
* Job matcher working ✅

---

## 👨‍💻 Author

Manikonda Sai Thriguna
B.Tech AIML

🔗 GitHub: https://github.com/Thriguna333
