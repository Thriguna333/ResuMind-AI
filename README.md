# 🧠 ResuMind AI

AI-powered Resume & Document Intelligence Platform using RAG, semantic search, local LLMs, and job matching.

## 🚀 Features

- 📄 Resume analysis with score, strengths, and improvement suggestions
- 📚 Document/report extraction for PDF, DOCX, and PPTX files
- 💬 RAG-based chat with uploaded resumes and documents
- 🎯 Job description matching with matched and missing skills
- 🤖 AI recruiter feedback using local Ollama model
- 🧠 Blackbox AI for general AI assistance
- 🔍 Semantic search using Qdrant vector database
- 📊 Professional Streamlit dashboard

## 🛠 Tech Stack

- Python
- FastAPI
- Streamlit
- Qdrant
- Sentence Transformers
- spaCy
- Ollama / Phi-3
- PyMuPDF
- python-docx
- python-pptx

## 🧩 System Architecture

1. User uploads resume/document
2. Text and metadata are extracted
3. Text is cleaned and split into chunks
4. Chunks are converted into embeddings
5. Embeddings are stored in Qdrant
6. User asks questions
7. Relevant chunks are retrieved
8. Local LLM generates grounded answers

## 📌 Modules

### Resume Intelligence
Extracts candidate details, skills, projects, education, resume score, and recruiter-style feedback.

### Document Intelligence
Extracts text, headings, tables, key-value pairs, and enables document-based Q&A.

### Job Matcher
Compares resume skills with job description requirements and returns a match score.

### Blackbox AI
Provides general AI assistance using a local LLM.

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Thriguna333/ResuMind-AI.git
cd ResuMind-AI/backend