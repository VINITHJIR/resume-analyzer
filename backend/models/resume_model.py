from sqlalchemy import Column, Integer, String, LargeBinary , DateTime , ForeignKey
from database import Base
from datetime import datetime

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)
    file_data = Column(LargeBinary)   # 🔥 PDF stored here

    score = Column(Integer)
    strengths = Column(String)
    weakness = Column(String)
    suggestions = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))  # 🔥 IMPORTANT