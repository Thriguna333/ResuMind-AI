import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"


import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"


def smart_extract(query, data):
    q = query.lower()

    intel = data.get("resume_intelligence", {})

    if "name" in q:
        return intel.get("name")

    if "email" in q:
        return intel.get("email")

    if "phone" in q:
        return intel.get("phone")

    if "location" in q:
        return intel.get("location")

    if "skills" in q:
        return ", ".join(intel.get("skills", []))

    if "education" in q:
        return str(intel.get("education"))

    return None


def generate_answer(query, results, parsed_data):
    if not results:
        return {
            "answer": "No relevant information found.",
            "confidence": 0,
            "citations": []
        }

    # 🔥 Step 1: Filter top useful chunks
    filtered = [r for r in results if r["score"] > 0.2]

    if not filtered:
        filtered = results

    # 🔥 Step 2: Take top 3 only
    filtered = filtered[:3]

    # 🔥 Step 3: Build clean context
    context = "\n\n".join([r["text"] for r in filtered])

    # 🔥 Step 4: Better prompt
    prompt = f"""
You are an intelligent document assistant.

Use ONLY the context below to answer the question.

If the answer is not clearly present, say "Not found in document".

Context:
{context}

Question:
{query}

Give a clear and complete answer:
"""

    # 🔥 Step 5: Call Ollama
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 80,
                "temperature": 0.2
            }
        }
    )

    answer = response.json().get("response", "").strip()

    # 🔥 Step 6: Confidence
    confidence = sum(r["score"] for r in filtered) / len(filtered)

    # 🔥 Step 7: Citations
    citations = []
    for r in filtered:
        citations.append({
            "source": r["filename"],
            "chunk": r["chunk_number"],
            "score": r["score"]
        })

    return {
        "answer": answer,
        "confidence": round(confidence, 3),
        "citations": citations
    }