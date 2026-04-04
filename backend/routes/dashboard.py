from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.resume_model import Resume
from utils.dependencies import get_current_user

router = APIRouter()

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Dashboard API
@router.get("/my-resumes")
def get_my_resumes(user=Depends(get_current_user), db: Session = Depends(get_db)):

    # 🔥 Admin → all data
    if user["role"] == "admin":
        resumes = db.query(Resume).all()
    else:
        # 🔥 User → only their data
        resumes = db.query(Resume).filter(
            Resume.user_id == user["user_id"]
        ).all()

    # ✅ Clean response (NO binary)
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "score": r.score,
            "strengths": r.strengths,
            "weakness": r.weakness,
            "suggestions": r.suggestions
        }
        for r in resumes
    ]