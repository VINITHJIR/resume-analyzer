from fastapi import FastAPI
from routes import upload, dashboard ,auth
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import rag
from models import user_model, resume_model
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(rag.router)