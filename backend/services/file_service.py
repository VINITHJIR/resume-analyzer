from services.parser import extract_text
from services.ai_service import analyze_resume, extract_json
import pdfplumber
import io
async def save_file(file , job_description=None):
    # 🔥 Read file directly
    file_bytes = await file.read()

    # 🔥 Extract text (must support bytes)
    text = extract_text(file_bytes)

    # 🔥 AI
    ai_raw = analyze_resume(text , job_description)
    ai_result = extract_json(ai_raw)

    return file.filename, file_bytes, text, ai_result



def extract_text(file_bytes):
    text = ""

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text