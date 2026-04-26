import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def analyze_resume(text):
    text_lower = text.lower()

    email = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    phone = re.findall(r"\b\d{10}\b", text)

    skills_list = [
        "python", "java", "sql", "machine learning", "nlp",
        "power bi", "excel", "tableau", "git", "html"
    ]

    skills_found = [skill for skill in skills_list if skill in text_lower]

    score = 0
    feedback = []
    strengths = []

    if len(skills_found) >= 5:
        score += 25
        strengths.append("Strong technical skills")
    else:
        score += len(skills_found) * 3
        feedback.append("Add more technical skills")

    if "project" in text_lower:
        score += 20
        strengths.append("Projects section present")
    else:
        feedback.append("Add projects")

    if "internship" in text_lower or "experience" in text_lower:
        score += 15
        strengths.append("Experience present")
    else:
        feedback.append("Add internship/experience")

    if "education" in text_lower:
        score += 15
    else:
        feedback.append("Add education section")

    if email:
        score += 10
    else:
        feedback.append("Missing email")

    if phone:
        score += 10
    else:
        feedback.append("Missing phone number")

    if "ai" in text_lower or "machine learning" in text_lower:
        score += 5
        strengths.append("AI/ML profile")

    if score > 100:
        score = 100

    return {
        "score": score,
        "skills_found": skills_found,
        "email": email[0] if email else None,
        "phone": phone[0] if phone else None,
        "strengths": strengths,
        "feedback": feedback
    }


def generate_ai_resume_feedback(text):
    prompt = f"""
You are an HR recruiter.

Analyze this resume and give:

1. Overall impression
2. Strengths
3. Weak areas
4. Suggestions to improve
5. Best roles

Resume:
{text[:3000]}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.2
                }
            },
            timeout=60
        )

        if response.status_code != 200:
            return "AI feedback not available."

        return response.json().get("response", "").strip()

    except Exception as e:
        return f"AI feedback error: {str(e)}"