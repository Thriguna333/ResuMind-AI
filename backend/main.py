from fastapi import FastAPI, UploadFile, File
import os

from backend.utils.file_parser import parse_file
from utils.vector_store import create_collection, store_document, search, reset_collection
from utils.qa_engine import generate_answer
from utils.resume_analyzer import analyze_resume
from job_matcher import match_resume_to_job

app = FastAPI(title="Document Intelligence Pipeline")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_parsed_data = {}


@app.get("/")
def home():
    return {"message": "Backend running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global latest_parsed_data

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    file_type = file.filename.split(".")[-1].lower()
    parsed_data = parse_file(file_path, file_type)

    latest_parsed_data = parsed_data

    extracted_text = parsed_data["full_text"]

    resume_analysis = analyze_resume(extracted_text)
    ai_resume_feedback = "AI feedback not generated yet. Use /ai-feedback endpoint."

    create_collection()

    num_chunks = store_document(extracted_text, {
        "filename": file.filename
    })

    return {
        "status": "success",
        "filename": file.filename,
        "file_type": file_type,
        "total_characters": len(extracted_text),
        "total_words": len(extracted_text.split()),
        "total_pages": len(parsed_data["pages"]),
        "extracted_text_preview": extracted_text[:1000],
        "headings": parsed_data.get("headings", []),
        "tables": parsed_data.get("tables", []),
        "key_value_pairs": parsed_data.get("key_value_pairs", {}),
        "entities": parsed_data.get("entities", []),
        "resume_intelligence": parsed_data.get("resume_intelligence", {}),
        "resume_analysis": resume_analysis,
        "ai_resume_feedback": ai_resume_feedback,
        "pages": parsed_data["pages"],
        "stored_chunks": num_chunks,
    }


@app.get("/search")
def search_docs(query: str):
    try:
        results = search(query, top_k=3)
        answer_data = generate_answer(query, results, latest_parsed_data)

        return {
            "query": query,
            "answer": answer_data.get("answer"),
            "confidence": answer_data.get("confidence", 0),
            "citations": answer_data.get("citations", []),
            "results": results
        }

    except Exception as e:
        return {
            "query": query,
            "answer": f"Error: {str(e)}",
            "confidence": 0,
            "citations": [],
            "results": []
        }


@app.post("/match-job")
async def match_job(job_description: str):
    global latest_parsed_data

    if not latest_parsed_data:
        return {
            "error": "Please upload a resume first."
        }

    result = match_resume_to_job(latest_parsed_data, job_description)
    return result


@app.post("/reset-vector-db")
def reset_vector_db():
    reset_collection()
    return {
        "status": "success",
        "message": "Vector database reset successfully"
    }


@app.get("/ai-feedback")
def ai_feedback():
    global latest_parsed_data

    if not latest_parsed_data:
        return {
            "feedback": "Please upload a resume first."
        }

    text = latest_parsed_data.get("full_text", "")
    feedback = generate_ai_resume_feedback(text)

    return {
        "feedback": feedback
    }


@app.post("/blackbox-ai")
def blackbox_ai(prompt: str):
    import requests

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 120,
                    "temperature": 0.4
                }
            }
        )

        answer = response.json().get("response", "")

        return {
            "answer": answer
        }

    except Exception as e:
        return {
            "answer": f"Error: {str(e)}"
        }