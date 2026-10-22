# ============================================================
# RESUME API ROUTES
# ============================================================

import os
import shutil
import json
from typing import Optional
from app.services.ats_checker import (
    check_ats,
    check_resume_ats_score,
)
from app.api.users import get_current_user

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.resume import Resume

from app.models.analysis import (
    ResumeAnalysis,
    InterviewHistory
)
from app.models.skill_progress import SkillProgress

from app.services.pdf_parser import (
    extract_text_from_pdf
)

from app.services.resume_analyzer import (
    analyze_resume,
    extract_skills,
    get_flattened_skills,
    find_missing_skills,
    calculate_job_match,
    extract_required_skills_from_job
)

from app.services.semantic_matcher import (
    calculate_semantic_similarity
)

from app.services.recommendation_engine import (
    generate_recommendations
)

from app.services.interview_generator import (
    generate_interview_questions,
    evaluate_interview_answer
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# ============================================================
# INTERVIEW ANSWER REQUEST
# ============================================================

class InterviewAnswerRequest(BaseModel):

    question: str

    answer: str

    job_description: str

    time_taken: int

    time_limit: Optional[int] = 90

    # Interview question metadata
    skill: Optional[str] = "General"

    question_type: Optional[str] = "Technical"

    difficulty: Optional[str] = "Medium"

# ============================================================
# SKILL PROGRESS REQUEST
# ============================================================

class SkillProgressRequest(BaseModel):

    skill: str

    status: str


# ============================================================
# UPLOAD RESUME
# ============================================================

@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # --------------------------------------------------------
    # Check file type
    # --------------------------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )


    # --------------------------------------------------------
    # Create file path
    # --------------------------------------------------------

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )


    # --------------------------------------------------------
    # Save uploaded file
    # --------------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    extracted_text = extract_text_from_pdf(
        file_path
    )


    # --------------------------------------------------------
    # Create resume record
    # --------------------------------------------------------



    resume = Resume(
        user_id=current_user["id"],
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text
    )


    db.add(resume)

    db.commit()

    db.refresh(resume)


    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return {

        "message":
            "Resume uploaded successfully",

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "text_length":
            len(extracted_text)

    }


# ============================================================
# ANALYZE RESUME
# ============================================================

@router.get("/{resume_id}/analyze")
def analyze_uploaded_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):

    # Find resume

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    # Analyze resume

    analysis = analyze_resume(
        resume.extracted_text
    )


    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "analysis":
            analysis

    }


# ============================================================
# MISSING SKILLS
# ============================================================

@router.post("/{resume_id}/missing-skills")
def get_missing_skills(
    resume_id: int,
    required_skills: list[str],
    db: Session = Depends(get_db)
):

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    # Extract skills

    found_skills_by_category = extract_skills(
        resume.extracted_text
    )


    resume_skills = get_flattened_skills(
        found_skills_by_category
    )


    # Find missing skills

    missing_skills = find_missing_skills(
        resume_skills,
        required_skills
    )


    # Calculate match

    match_percentage = calculate_job_match(
        resume_skills,
        required_skills
    )


    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "resume_skills":
            resume_skills,

        "required_skills":
            required_skills,

        "missing_skills":
            missing_skills,

        "job_match_percentage":
            match_percentage

    }


# ============================================================
# JOB MATCH
# ============================================================

@router.post("/{resume_id}/job-match")
def analyze_job_match(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    # Resume skills

    resume_skills_by_category = extract_skills(
        resume.extracted_text
    )


    resume_skills = get_flattened_skills(
        resume_skills_by_category
    )


    # Job skills

    required_skills = extract_required_skills_from_job(
        job_description
    )


    # Missing skills

    missing_skills = find_missing_skills(
        resume_skills,
        required_skills
    )


    # Calculate match

    match_percentage = calculate_job_match(
        resume_skills,
        required_skills
    )


    # Matched skills

    matched_skills = [

        skill

        for skill in required_skills

        if skill not in missing_skills

    ]


    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "job_match_percentage":
            match_percentage

    }


# ============================================================
# SEMANTIC MATCH
# ============================================================

@router.post("/{resume_id}/semantic-match")
def semantic_match(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    similarity = calculate_semantic_similarity(

        resume.extracted_text,

        job_description

    )


    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "semantic_match_percentage":
            similarity

    }


# ============================================================
# FINAL MATCH
# ============================================================

@router.post("/{resume_id}/final-match")
def final_match(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):

    # Find resume

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    # Extract resume skills

    resume_skills_by_category = extract_skills(
        resume.extracted_text
    )


    resume_skills = get_flattened_skills(
        resume_skills_by_category
    )


    # Extract job skills

    required_skills = extract_required_skills_from_job(
        job_description
    )


    # Calculate skill match

    skill_match = calculate_job_match(
        resume_skills,
        required_skills
    )


    # Find missing skills

    missing_skills = find_missing_skills(
        resume_skills,
        required_skills
    )


    # Semantic match

    semantic_match = calculate_semantic_similarity(

        resume.extracted_text,

        job_description

    )


    # Final score

    final_score = (

        skill_match * 0.60

        +

        semantic_match * 0.40

    )


    # Matched skills

    matched_skills = [

        skill

        for skill in required_skills

        if skill not in missing_skills

    ]


    # Save analysis

    analysis_record = ResumeAnalysis(

        resume_id=resume.id,

        job_description=job_description,

        skill_match_percentage=skill_match,

        semantic_match_percentage=semantic_match,

        final_match_percentage=round(
            final_score,
            2
        ),

        matched_skills=json.dumps(
            matched_skills
        ),

        missing_skills=json.dumps(
            missing_skills
        )

    )


    db.add(
        analysis_record
    )

    db.commit()

    db.refresh(
        analysis_record
    )


    # Return result

    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "skill_match_percentage":
            skill_match,

        "semantic_match_percentage":
            semantic_match,

        "final_match_percentage":
            round(
                final_score,
                2
            ),

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills

    }


# ============================================================
# RECOMMENDATIONS
# ============================================================

@router.post("/{resume_id}/recommendations")
def get_recommendations(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find resume
    # --------------------------------------------------------

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )

    # --------------------------------------------------------
    # Resume skills
    # --------------------------------------------------------

    resume_skills_by_category = extract_skills(
        resume.extracted_text
    )

    resume_skills = get_flattened_skills(
        resume_skills_by_category
    )

    # --------------------------------------------------------
    # Job skills
    # --------------------------------------------------------

    required_skills = extract_required_skills_from_job(
        job_description
    )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing_skills = find_missing_skills(
        resume_skills,
        required_skills
    )

    # --------------------------------------------------------
    # Get interview history
    # --------------------------------------------------------

    interview_history = db.query(
        InterviewHistory
    ).filter(
        InterviewHistory.resume_id == resume_id
    ).all()

    # --------------------------------------------------------
    # Generate smart recommendations
    # --------------------------------------------------------

    recommendations = generate_recommendations(
        missing_skills,
        interview_history
    )

    # --------------------------------------------------------
    # Return response
    # --------------------------------------------------------

    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "resume_skills":
            resume_skills,

        "required_skills":
            required_skills,

        "missing_skills":
            missing_skills,

        "recommendations":
            recommendations

    }


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

@router.post("/{resume_id}/interview-questions")
def get_interview_questions(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db)
):

    # Find resume

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    if not resume.extracted_text:

        raise HTTPException(
            status_code=400,
            detail="No text found in resume"
        )


    # Extract resume skills

    resume_skills_by_category = extract_skills(
        resume.extracted_text
    )


    resume_skills = get_flattened_skills(
        resume_skills_by_category
    )


    # Extract job skills

    job_skills = extract_required_skills_from_job(
        job_description
    )


    # --------------------------------------------------------
    # Combine skills
    # --------------------------------------------------------

    combined_skills = list(
        dict.fromkeys(
            resume_skills
            +
            job_skills
        )
    )

    # --------------------------------------------------------
    # Generate personalized interview questions
    # --------------------------------------------------------

    questions = generate_interview_questions(
        skills=combined_skills,
        number_of_questions=15,
        resume_text=resume.extracted_text,
        job_description=job_description,
        resume_skills=resume_skills,
        job_skills=job_skills
    )


   # --------------------------------------------------------
    # Return questions
    # --------------------------------------------------------

    return {
        "resume_id": resume.id,
        "filename": resume.filename,

        "resume_skills": resume_skills,

        "job_skills": job_skills,   

        "matched_skills": [
            skill
            for skill in job_skills
            if skill not in find_missing_skills(
                resume_skills,
                job_skills
            )
        ],

        "missing_skills": find_missing_skills(
            resume_skills,
            job_skills
        ),

        "skills_used": combined_skills,

        "total_questions": len(questions),

        "questions": questions
    }

# ============================================================
# EVALUATE INTERVIEW ANSWER
# ============================================================

@router.post("/{resume_id}/evaluate-answer")
def evaluate_interview_answer_route(

    resume_id: int,

    request: InterviewAnswerRequest,

    db: Session = Depends(get_db)

):

    # --------------------------------------------------------
    # Find resume
    # --------------------------------------------------------

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    # --------------------------------------------------------
    # Validate answer
    # --------------------------------------------------------

    if not request.answer.strip():

        raise HTTPException(
            status_code=400,
            detail="Answer cannot be empty"
        )


    # --------------------------------------------------------
    # Validate time values
    # --------------------------------------------------------

    time_limit = (
        request.time_limit
        if request.time_limit is not None
        else 90
    )

    time_taken = max(
        0,
        min(
            request.time_taken,
            time_limit
        )
    )


    # --------------------------------------------------------
    # Evaluate answer
    # --------------------------------------------------------

    evaluation = evaluate_interview_answer(

        question=request.question,

        answer=request.answer,

        job_description=request.job_description,

        time_taken=time_taken,

        time_limit=time_limit

    )


    # --------------------------------------------------------
    # Safely get evaluation values
    # --------------------------------------------------------

    if not isinstance(
        evaluation,
        dict
    ):

        raise HTTPException(
            status_code=500,
            detail="Invalid evaluation response"
        )


    score = evaluation.get(
        "score",
        evaluation.get(
            "overall_score",
            0
        )
    )

    relevance_score = evaluation.get(
        "relevance_score",
        0
    )

    technical_score = evaluation.get(
        "technical_score",
        0
    )

    project_score = evaluation.get(
        "project_score",
        0
    )

    communication_score = evaluation.get(
        "communication_score",
        0
    )

    time_score = evaluation.get(
        "time_score",
        0
    )


    # --------------------------------------------------------
    # Get question information
    # --------------------------------------------------------

    # Use metadata sent by the frontend.
    # These values come from the generated interview question.

    skill = request.skill or "General"

    question_type = request.question_type or "Technical"

    difficulty = request.difficulty or "Medium"


    # --------------------------------------------------------
    # Get feedback information
    # --------------------------------------------------------

    feedback = evaluation.get(
        "feedback",
        ""
    )

    strengths = evaluation.get(
        "strengths",
        []
    )

    improvements = evaluation.get(
        "improvements",
        []
    )

    matched_topics = evaluation.get(
        "matched_topics",
        []
    )

    project_topics = evaluation.get(
        "project_topics",
        []
    )


    # --------------------------------------------------------
    # SAVE INTERVIEW HISTORY
    # --------------------------------------------------------

    history_record = InterviewHistory(

        resume_id=resume.id,

        question=request.question,

        answer=request.answer,

        skill=skill,

        question_type=question_type,

        difficulty=difficulty,

        score=float(score or 0),

        relevance_score=float(
            relevance_score or 0
        ),

        technical_score=float(
            technical_score or 0
        ),

        project_score=float(
            project_score or 0
        ),

        communication_score=float(
            communication_score or 0
        ),

        time_score=float(
            time_score or 0
        ),

        time_taken=time_taken,

        time_limit=time_limit,

        feedback=str(
            feedback or ""
        ),

        strengths=json.dumps(
            strengths
            if isinstance(
                strengths,
                list
            )
            else [strengths]
        ),

        improvements=json.dumps(
            improvements
            if isinstance(
                improvements,
                list
            )
            else [improvements]
        ),

        matched_topics=json.dumps(
            matched_topics
            if isinstance(
                matched_topics,
                list
            )
            else [matched_topics]
        ),

        project_topics=json.dumps(
            project_topics
            if isinstance(
                project_topics,
                list
            )
            else [project_topics]
        ),

        skipped=0

    )


    db.add(
        history_record
    )

    db.commit()

    db.refresh(
        history_record
    )


    # --------------------------------------------------------
    # Return evaluation
    # --------------------------------------------------------

    return {

        "resume_id":
            resume.id,

        "question":
            request.question,

        "answer":
            request.answer,

        "evaluation":
            evaluation,

        "history_id":
            history_record.id,

        "saved_to_history":
            True

    }


# ============================================================
# HISTORY
# ============================================================

@router.get("/{resume_id}/history")
def get_resume_history(
    resume_id: int,
    db: Session = Depends(get_db)
):

    # Find resume

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()


    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )


    # Get analyses

    analyses = db.query(
        ResumeAnalysis
    ).filter(
        ResumeAnalysis.resume_id == resume_id
    ).order_by(
        ResumeAnalysis.created_at.desc()
    ).all()


    history = []


    # Format history

    for analysis in analyses:

        history.append({

            "analysis_id":
                analysis.id,

            "job_description":
                analysis.job_description,

            "skill_match_percentage":
                analysis.skill_match_percentage,

            "semantic_match_percentage":
                analysis.semantic_match_percentage,

            "final_match_percentage":
                analysis.final_match_percentage,

            "matched_skills":

                json.loads(
                    analysis.matched_skills
                )
                if analysis.matched_skills
                else [],

            "missing_skills":

                json.loads(
                    analysis.missing_skills
                )
                if analysis.missing_skills
                else [],

            "created_at":
                analysis.created_at

        })


    # Return history

    return {

        "resume_id":
            resume.id,

        "filename":
            resume.filename,

        "total_analyses":
            len(history),

        "history":
            history

    }

# ============================================================
# INTERVIEW HISTORY
# ============================================================

@router.get("/{resume_id}/interview-history")
def get_interview_history(
    resume_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find resume
    # --------------------------------------------------------

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Get interview history
    # --------------------------------------------------------

    interviews = db.query(
        InterviewHistory
    ).filter(
        InterviewHistory.resume_id == resume_id
    ).order_by(
        InterviewHistory.created_at.desc()
    ).all()

    history = []

    # --------------------------------------------------------
    # Format interview history
    # --------------------------------------------------------

    for interview in interviews:

        history.append({
            "id": interview.id,

            "question": interview.question,

            "answer": interview.answer,

            "skill": interview.skill,

            "question_type": interview.question_type,

            "difficulty": interview.difficulty,

            "score": interview.score,

            "relevance_score":
                interview.relevance_score,

            "technical_score":
                interview.technical_score,

            "project_score":
                interview.project_score,

            "communication_score":
                interview.communication_score,

            "time_score":
                interview.time_score,

            "time_taken":
                interview.time_taken,

            "time_limit":
                interview.time_limit,

            "feedback":
                interview.feedback,

            "strengths":
                json.loads(
                    interview.strengths
                )
                if interview.strengths
                else [],

            "improvements":
                json.loads(
                    interview.improvements
                )
                if interview.improvements
                else [],

            "matched_topics":
                json.loads(
                    interview.matched_topics
                )
                if interview.matched_topics
                else [],

            "project_topics":
                json.loads(
                    interview.project_topics
                )
                if interview.project_topics
                else [],

            "skipped":
                interview.skipped,

            "created_at":
                interview.created_at
        })

    # --------------------------------------------------------
    # Return interview history
    # --------------------------------------------------------

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "total_interviews": len(history),
        "history": history
    }

# ============================================================
# SKILL PROGRESS
# ============================================================

@router.put("/{resume_id}/skill-progress")
def update_skill_progress(
    resume_id: int,
    data: SkillProgressRequest,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Validate status
    # --------------------------------------------------------

    valid_statuses = [
        "NOT STARTED",
        "IN PROGRESS",
        "COMPLETED"
    ]

    if data.status not in valid_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid skill progress status"
        )

    # --------------------------------------------------------
    # Check resume
    # --------------------------------------------------------

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Find existing progress
    # --------------------------------------------------------

    progress = db.query(
        SkillProgress
    ).filter(
        SkillProgress.resume_id == resume_id,
        SkillProgress.skill.ilike(data.skill)
    ).first()

    # --------------------------------------------------------
    # Update existing progress
    # --------------------------------------------------------

    if progress:

        progress.status = data.status

    # --------------------------------------------------------
    # Create new progress
    # --------------------------------------------------------

    else:

        progress = SkillProgress(
            resume_id=resume_id,
            skill=data.skill,
            status=data.status
        )

        db.add(progress)

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    db.commit()

    db.refresh(progress)

    return {
        "message": "Skill progress updated successfully",
        "resume_id": progress.resume_id,
        "skill": progress.skill,
        "status": progress.status,
        "updated_at": progress.updated_at
    }

# ============================================================
# GET SKILL PROGRESS
# ============================================================

@router.get("/{resume_id}/skill-progress")
def get_skill_progress(
    resume_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Check resume
    # --------------------------------------------------------

    resume = db.query(
        Resume
    ).filter(
        Resume.id == resume_id
    ).first()

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    # --------------------------------------------------------
    # Get progress
    # --------------------------------------------------------

    progress = db.query(
        SkillProgress
    ).filter(
        SkillProgress.resume_id == resume_id
    ).order_by(
        SkillProgress.skill.asc()
    ).all()

    # --------------------------------------------------------
    # Return progress
    # --------------------------------------------------------

    return {
        "resume_id": resume_id,

        "progress": [
            {
                "id": item.id,
                "skill": item.skill,
                "status": item.status,
                "updated_at": item.updated_at
            }

            for item in progress
        ]
    }


@router.post("/{resume_id}/ats-check")
def ats_check_resume(
    resume_id: int,
    job_description: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user["id"],
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No extracted text found for this resume",
        )

    try:
        return check_ats(
            resume_text=resume.extracted_text,
            job_description=job_description,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/{resume_id}/ats-score")
def ats_score_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user["id"],
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No extracted text found for this resume",
        )

    
    try:
        result = check_resume_ats_score(
            resume_text=resume.extracted_text,
        )

        print("ATS DEBUG - Resume ID:", resume.id)
        print("ATS DEBUG - Filename:", resume.filename)
        print("ATS DEBUG - Score:", result.get("ats_score"))
        print("ATS DEBUG - Breakdown:", result.get("score_breakdown"))
        print("ATS DEBUG - Sections:", result.get("sections_found"))
        print("ATS DEBUG - Sections with content:", result.get("sections_with_content"))

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )