import re


SKILLS = {
    "programming": [
        "Python",
        "Java",
        "C++",
        "C",
        "C#",
        "JavaScript"
    ],

    "frontend": [
        "HTML",
        "CSS",
        "React",
        "Angular",
        "Vue",
        "Bootstrap",
        "Tailwind CSS"
    ],

    "backend": [
        "FastAPI",
        "Flask",
        "Django",
        "Node.js",
        "Express.js"
    ],

    "database": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "SQLite"
    ],

    "ai_ml": [
        "Artificial Intelligence",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Natural Language Processing",
        "Computer Vision",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn"
    ],

    "tools": [
        "Git",
        "GitHub",
        "Docker",
        "AWS",
        "Linux"
    ]
}


def normalize_text(text: str) -> str:
    return text.lower()


def extract_skills(text: str) -> dict:

    text = normalize_text(text)

    found_skills = {}

    for category, skills in SKILLS.items():

        found_skills[category] = []

        for skill in skills:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, text):
                found_skills[category].append(skill)

    return found_skills


def get_all_skills() -> list:

    all_skills = []

    for skills in SKILLS.values():
        all_skills.extend(skills)

    return all_skills


def get_flattened_skills(found_skills: dict) -> list:

    skills = []

    for category_skills in found_skills.values():
        skills.extend(category_skills)

    return skills


def calculate_score(found_skills: dict) -> int:

    total_skills = len(get_all_skills())

    found_count = len(
        get_flattened_skills(found_skills)
    )

    if total_skills == 0:
        return 0

    score = (found_count / total_skills) * 100

    return round(score)


def find_missing_skills(
    resume_skills: list,
    required_skills: list
) -> list:

    resume_skills_lower = {
        skill.lower()
        for skill in resume_skills
    }

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in resume_skills_lower:
            missing_skills.append(skill)

    return missing_skills


def calculate_job_match(
    resume_skills: list,
    required_skills: list
) -> int:

    if not required_skills:
        return 0

    resume_skills_lower = {
        skill.lower()
        for skill in resume_skills
    }

    matched = 0

    for skill in required_skills:

        if skill.lower() in resume_skills_lower:
            matched += 1

    match_percentage = (
        matched / len(required_skills)
    ) * 100

    return round(match_percentage)


def analyze_resume(text: str) -> dict:

    found_skills = extract_skills(text)

    score = calculate_score(found_skills)

    return {
        "score": score,
        "skills": found_skills
    }

def extract_required_skills_from_job(
    job_description: str
) -> list:

    found_skills = extract_skills(
        job_description
    )

    required_skills = get_flattened_skills(
        found_skills
    )

    return required_skills