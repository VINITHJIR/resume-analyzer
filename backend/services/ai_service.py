import requests
import json
import os
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
def analyze_resume(text):
    try:
        print("Using Groq...")
        return groq_call(text)

    except Exception as e:
        print("Groq failed:", e)

        try:
            print("Falling back to DeepSeek...")
            return deepseek_call(text)

        except Exception as e:
            print("DeepSeek also failed:", e)
            return "{}"


# ==============================
# GROQ FUNCTION
# ==============================
def groq_call(text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a resume analyzer.
Return ONLY JSON.

Format:
{{
  "score": 85,
  "strengths": "text",
  "weakness": "text",
  "suggestions": "text"
}}

Resume:
{text[:800]}
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
# DEEPSEEK FUNCTION (Fallback)
# ==============================
def deepseek_call(text):
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": text[:500]}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    print("DeepSeek RAW RESPONSE:", response.text)  # 🔥 DEBUG

    data = response.json()

    if "choices" not in data:
        raise Exception(f"DeepSeek API Error: {data}")

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
            "suggestions": data.get("suggestions", "")
        }

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        return {
            "score": 0,
            "strengths": "",
            "weakness": "",
            "suggestions": ""
        }