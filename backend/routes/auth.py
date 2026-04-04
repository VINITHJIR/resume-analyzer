from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from utils.password import hash_password, verify_password
from utils.jwt_handler import create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Register
@router.post("/register")
def register(user: dict, db: Session = Depends(get_db)):

    new_user = User(
        username=user["username"],
        email=user["email"],
        password=hash_password(user["password"]),
        phone=user["phone"],
        role="user"
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered"}

# ✅ Login
@router.post("/login")
def login(user: dict, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user["username"]
    ).first()

    if not db_user or not verify_password(user["password"], db_user.password):
        return {"error": "Invalid credentials"}

    token = create_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {"token": token}