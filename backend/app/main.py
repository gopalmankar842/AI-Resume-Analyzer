from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# ============================================================
# MODELS
# ============================================================
from app.models.skill_progress import SkillProgress
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import (
    ResumeAnalysis,
    InterviewHistory
)

# ============================================================
# API ROUTERS
# ============================================================

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.resume import router as resume_router


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Resume & Interview Analyzer",
    description="AI-powered resume analysis and interview preparation platform",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)

app.include_router(users_router)

app.include_router(resume_router)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Resume Analyzer API is running!"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }