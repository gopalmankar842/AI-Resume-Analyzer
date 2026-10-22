from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class ResumeAnalysis(Base):

    __tablename__ = "resume_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    job_description = Column(
        Text,
        nullable=False
    )

    skill_match_percentage = Column(
        Float,
        nullable=False
    )

    semantic_match_percentage = Column(
        Float,
        nullable=False
    )

    final_match_percentage = Column(
        Float,
        nullable=False
    )

    matched_skills = Column(
        Text,
        nullable=True
    )

    missing_skills = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

# ============================================================
# INTERVIEW HISTORY
# ============================================================

class InterviewHistory(Base):

    __tablename__ = "interview_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=True
    )

    skill = Column(
        Text,
        nullable=True
    )

    question_type = Column(
        Text,
        nullable=True
    )

    difficulty = Column(
        Text,
        nullable=True
    )

    score = Column(
        Float,
        nullable=False,
        default=0
    )

    relevance_score = Column(
        Float,
        nullable=False,
        default=0
    )

    technical_score = Column(
        Float,
        nullable=False,
        default=0
    )

    project_score = Column(
        Float,
        nullable=False,
        default=0
    )

    communication_score = Column(
        Float,
        nullable=False,
        default=0
    )

    time_score = Column(
        Float,
        nullable=False,
        default=0
    )

    time_taken = Column(
        Integer,
        nullable=False,
        default=0
    )

    time_limit = Column(
        Integer,
        nullable=False,
        default=90
    )

    feedback = Column(
        Text,
        nullable=True
    )

    strengths = Column(
        Text,
        nullable=True
    )

    improvements = Column(
        Text,
        nullable=True
    )

    matched_topics = Column(
        Text,
        nullable=True
    )

    project_topics = Column(
        Text,
        nullable=True
    )

    skipped = Column(
        Integer,
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )