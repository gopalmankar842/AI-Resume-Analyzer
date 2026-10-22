from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.database import Base


class SkillProgress(Base):

    __tablename__ = "skill_progress"

    id = Column(Integer, primary_key=True, index=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id"),
        nullable=False
    )

    skill = Column(
        String(100),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="NOT STARTED"
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "skill",
            name="unique_resume_skill_progress"
        ),
    )