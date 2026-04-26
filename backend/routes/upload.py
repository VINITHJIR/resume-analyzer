from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session

from database import SessionLocal
from models.resume_model import Resume
from services.file_service import save_file
from utils.dependencies import get_current_user   # 🔥 ADD THIS

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...), 
    job_description: str = Form(None),  
    user=Depends(get_current_user),   # 🔥 ADD THIS
    db: Session = Depends(get_db)
):
    filename, file_bytes, text, ai_result = await save_file(file , job_description)

    resume = Resume(
        filename=filename,
        file_data=file_bytes,
        score=ai_result.get("score", 0),
        strengths=ai_result.get("strengths", ""),
        weakness=ai_result.get("weakness", ""),
        keyskills=ai_result.get("keyskills", ""),  
        suggestions=ai_result.get("suggestions", ""),
        user_id=user["user_id"]   # 🔥 FIXED (dynamic)
    )

    db.add(resume)
    db.commit()

    return {
        "message": "File uploaded",
        "filename": filename,
        "score": ai_result.get("score", 0),
        "strengths": ai_result.get("strengths", ""),
        "weakness": ai_result.get("weakness", ""),
        "keyskills": ai_result.get("keyskills", ""),
        "suggestions": ai_result.get("suggestions", "")
    }