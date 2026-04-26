from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pandas as pd

# 🔥 LOAD MODEL
model = SentenceTransformer("all-mpnet-base-v2")

# 🔥 FILE PATH
DATA_PATH = r"C:\Users\VINITHJI\resume-dataset\Resume\Resume.csv"

# 🔥 CONNECT QDRANT
qdrant = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "resumes"

# 🔥 RESET COLLECTION
if qdrant.collection_exists(COLLECTION_NAME):
    qdrant.delete_collection(COLLECTION_NAME)

qdrant.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# 🔥 LOAD DATA
df = pd.read_csv(DATA_PATH)

# 🔥 SHUFFLE DATA
df = df.sample(frac=1).reset_index(drop=True)

texts = df["Resume_str"].dropna().tolist()
categories = df["Category"].dropna().tolist()

# 🔥 SPLITTER
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

# 🔥 CATEGORY NORMALIZATION
def normalize_category(cat):
    cat = str(cat).strip().lower().replace("-", " ")

    if "it" in cat or "information technology" in cat:
        return "information technology"
    elif "hr" in cat or "human" in cat:
        return "hr"
    elif "finance" in cat or "account" in cat:
        return "finance"
    else:
        return cat.replace("-", " ")

# 🔥 INSERT DATA
points = []
id_counter = 1

LIMIT = 500   # ✅ reduced limit

for i, text in enumerate(texts[:LIMIT]):
    
    # 🔹 progress log
    if i % 50 == 0:
        print(f"Processing {i}/{LIMIT} resumes...")

    chunks = splitter.split_text(text)
    category = normalize_category(categories[i])

    # 🔥 BATCH EMBEDDING (FAST)
    vectors = model.encode(chunks).tolist()

    for chunk, vector in zip(chunks, vectors):
        points.append({
            "id": id_counter,
            "vector": vector,
            "payload": {
                "text": chunk,
                "category": category
            }
        })
        id_counter += 1

# 🔥 BATCH UPSERT (IMPORTANT)
BATCH_SIZE = 500

for i in range(0, len(points), BATCH_SIZE):
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points[i:i+BATCH_SIZE]
    )
    print(f"Inserted batch {i//BATCH_SIZE + 1}")

# 🔥 FINAL OUTPUT
print("✅ Data inserted into Qdrant")

unique_categories = set([p["payload"]["category"] for p in points])
print("📊 Categories in DB:", unique_categories)