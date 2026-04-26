from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 🔥 ENV
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔥 MODEL
model = SentenceTransformer("all-mpnet-base-v2")

# 🔥 QDRANT
qdrant = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "resumes"

# 🔥 CATEGORY MAP (fallback)
CATEGORY_MAP = {
    "information technology": ["python", "developer", "software", "it", "backend"],
    "hr": ["hr", "recruiter", "hiring", "human resource"],
    "finance": ["finance", "account", "bank"]
}

# ==============================
# 🔥 KEYWORD DETECTION (FALLBACK)
# ==============================
def detect_category_keywords(query: str):
    query = query.lower()

    for category, keywords in CATEGORY_MAP.items():
        for word in keywords:
            if word in query:
                return category

    return None


# ==============================
# 🔥 GROQ DETECTION (PRIMARY)
# ==============================
def detect_category_groq(query: str):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"""
Classify the following text into ONLY one category.

Categories:
- Information Technology
- HR
- Finance

Rules:
- Return only category name
- No explanation
- Must be one of the given categories

Text:
{query[:500]}
"""

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        }

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        category = data["choices"][0]["message"]["content"].strip().lower()

        print("Groq category:", category)

        return category

    except Exception as e:
        print("Groq detection failed:", e)
        return None


# ==============================
# 🔥 FINAL DETECTOR (AI FIRST)
# ==============================
def detect_category(query: str):

    # 🔥 STEP 1: TRY AI
    category = detect_category_groq(query)

    if category:
        return category

    print("⚠️ Falling back to keyword detection...")

    # 🔥 STEP 2: FALLBACK
    return detect_category_keywords(query)


# ==============================
# 🔥 SEARCH FUNCTION
# ==============================
def search_resumes(query: str):
    try:
        query_vector = model.encode(query).tolist()

        category = detect_category(query)

        print("Detected category:", category)

        # ✅ WITH FILTER
        if category:
            results = qdrant.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=5,
                query_filter={
                    "must": [
                        {
                            "key": "category",
                            "match": {"value": category}
                        }
                    ]
                }
            )

            return [r.payload for r in results.points]

        # ✅ NO FILTER (LAST FALLBACK)
        results = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=5
        )

        return [r.payload for r in results.points]

    except Exception as e:
        print("Search failed:", e)
        return []