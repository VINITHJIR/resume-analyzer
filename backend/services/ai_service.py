import requests
import json
import os
from services.rag_service import search_resumes
from dotenv import load_dotenv
load_dotenv()
# ==============================
# CONFIG (use .env in real project)
# ==============================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


# ==============================
# MAIN FUNCTION
# ==============================

def get_rag_context(user_text):
    try:
        results = search_resumes(user_text)
        # take top 3 results only (important)
        context = "\n\n".join([r["text"] for r in results[:3]])

        return context

    except Exception as e:
        print("RAG failed:", e)
        return ""


def analyze_resume(text , job_description=None) :
    try:
        print("🔍 Fetching RAG context...")

        context = get_rag_context(text)

        print("Using Groq with RAG...")
        
        return groq_call(text, context , job_description)

    except Exception as e:
        print("Groq failed:", e)



# ==============================
# GROQ FUNCTION
# ==============================
def groq_call(text, context="" , job_description=None):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    if job_description:
        jd_part = f"\nJob Description:\n{job_description[:1500]}"
        keyskill_instruction = """
    - Extract missing skills required for this job
    - Return them as comma-separated values in "keyskills"
    """
    else:
        jd_part = ""
        keyskill_instruction = """
    - keyskills must be empty ""
    """

    prompt = f"""
You are an expert ATS resume analyzer.

Return ONLY JSON.

Strict Format:
{{
  "score": 85,
  "strengths": "text",
  "weakness": "text",
  "keyskills": "comma separated skills",
  "suggestions": "text"
}}

User Resume:
{text[:2000]}

Reference Resume Data:
{context[:4000]}

 {jd_part}

Instructions:
- Compare resume with reference data
- Give realistic score
- Identify missing skills
{keyskill_instruction}
- Provide actionable suggestions
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    

    data = response.json()
    if response.status_code == 429:
     print("Rate limit hit, retrying...")
    if "choices" not in data:
        raise Exception(f"Groq API Error: {data}")

    return data["choices"][0]["message"]["content"]



# ==============================
# JSON EXTRACTOR (UNCHANGED)
# ==============================
import re 

def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()

        # Extract JSON block safely
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group()

        data = json.loads(text)

        return {
            "score": data.get("score", 0),
            "strengths": data.get("strengths", ""),
            "weakness": data.get("weakness", ""),
            "keyskills": data.get("keyskills", ""), 
            "suggestions": data.get("suggestions", "")
        }

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return {
            "score": 0,
            "strengths": "",
            "weakness": "",
            "keyskills":"",
            "suggestions": ""
        }