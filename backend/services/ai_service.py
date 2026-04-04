import requests
import json
import re
def analyze_resume(text):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
               "prompt": f"""
You are a resume analyzer.

STRICT RULES:
- Return ONLY valid JSON
- Do NOT include explanation
- Do NOT include markdown
- Do NOT include text outside JSON

Format:
{{
  "score": 85,
  "strengths": "text",
  "weakness": "text",
  "suggestions": "text"
}}

Resume:
{text[:1000]}
""",
                "stream": False
            }
        )

        data = response.json()
        raw_output = data.get("response", "")

        return raw_output

    except Exception as e:
        print("AI ERROR:", e)
        return {}
    


def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()

        if text.startswith("{") and not text.endswith("}"):
            text += "}"

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