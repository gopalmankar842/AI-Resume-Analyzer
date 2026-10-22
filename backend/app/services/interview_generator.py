# ============================================================
# INTERVIEW QUESTION GENERATOR
# ============================================================

# ============================================================
# INTERVIEW QUESTION DATABASE
# ============================================================
import re
QUESTIONS = {

    "Python": {
        "technical": [
            "What are the main features of Python?",
            "Explain the difference between a list, tuple and set in Python.",
            "What is object-oriented programming in Python?",
            "How does exception handling work in Python?"
        ],
        "advanced": [
            "Explain decorators and generators in Python.",
            "How does Python memory management work?",
            "What is the difference between multiprocessing and multithreading in Python?"
        ]
    },

    "FastAPI": {
        "technical": [
            "What is FastAPI?",
            "Why would you use FastAPI instead of a traditional Python web framework?",
            "What is dependency injection in FastAPI?",
            "How do you create a REST API using FastAPI?"
        ],
        "advanced": [
            "How would you secure a FastAPI application?",
            "How would you handle authentication using JWT in FastAPI?",
            "How would you optimize a FastAPI application for high traffic?"
        ]
    },

    "React": {
        "technical": [
            "What is React?",
            "What are React components?",
            "What are React hooks?",
            "What is the difference between props and state?"
        ],
        "advanced": [
            "Explain the React virtual DOM.",
            "How would you optimize a React application?",
            "What is the purpose of useEffect and useMemo?"
        ]
    },

    "PostgreSQL": {
        "technical": [
            "What is PostgreSQL?",
            "What is a primary key?",
            "What is a foreign key?",
            "What is the difference between SQL and NoSQL databases?"
        ],
        "advanced": [
            "What is database indexing?",
            "How would you optimize a slow PostgreSQL query?",
            "Explain database normalization."
        ]
    },

    "Machine Learning": {
        "technical": [
            "What is Machine Learning?",
            "What is the difference between supervised and unsupervised learning?",
            "What is overfitting?",
            "What is the difference between classification and regression?"
        ],
        "advanced": [
            "Explain the bias-variance tradeoff.",
            "How do you handle an imbalanced dataset?",
            "How would you select the best features for a machine learning model?"
        ]
    },

    "Deep Learning": {
        "technical": [
            "What is Deep Learning?",
            "What is an artificial neural network?",
            "What is an activation function?",
            "What is backpropagation?"
        ],
        "advanced": [
            "Explain vanishing and exploding gradients.",
            "What is the difference between CNN and RNN?",
            "Why are transformers useful for modern AI applications?"
        ]
    },

    "NLP": {
        "technical": [
            "What is Natural Language Processing?",
            "What is tokenization?",
            "What are word embeddings?",
            "What is the difference between stemming and lemmatization?"
        ],
        "advanced": [
            "What are transformer models?",
            "How does attention work in NLP?",
            "What is the difference between BERT and traditional word embeddings?"
        ]
    },

    "TensorFlow": {
        "technical": [
            "What is TensorFlow?",
            "What is Keras?",
            "How do you create a neural network using TensorFlow?"
        ],
        "advanced": [
            "How do you prevent overfitting in a TensorFlow model?",
            "How would you save and deploy a TensorFlow model?"
        ]
    },

    "PyTorch": {
        "technical": [
            "What is PyTorch?",
            "What is a tensor?",
            "What is the purpose of autograd in PyTorch?"
        ],
        "advanced": [
            "How does automatic differentiation work in PyTorch?",
            "How would you train and save a PyTorch model?"
        ]
    },

    "Git": {
        "technical": [
            "What is Git?",
            "What is the difference between Git and GitHub?",
            "What is a Git branch?",
            "How do you resolve a Git merge conflict?"
        ],
        "advanced": [
            "Explain Git rebase.",
            "What is the difference between merge and rebase?"
        ]
    },

    "Docker": {
        "technical": [
            "What is Docker?",
            "What is a Docker container?",
            "What is a Docker image?",
            "Why is Docker useful for deployment?"
        ],
        "advanced": [
            "What is the difference between a Docker image and container?",
            "How would you Dockerize a FastAPI application?",
            "How can Docker improve application portability?"
        ]
    },

    "AWS": {
        "technical": [
            "What is AWS?",
            "What is Amazon EC2?",
            "What is Amazon S3?",
            "Why is cloud deployment useful?"
        ],
        "advanced": [
            "How would you deploy a FastAPI application on AWS?",
            "How would you secure an AWS application?",
            "What is the difference between EC2 and serverless deployment?"
        ]
    }
}


# ============================================================
# TIME LIMITS
# ============================================================

INTERVIEW_TIME_LIMITS = {

    "Easy": 60,
    "Medium": 90,
    "Hard": 120
}


def generate_interview_questions(
    skills: list = None,
    number_of_questions: int = 15,
    resume_text: str = "",
    job_description: str = "",
    resume_skills: list = None,
    job_skills: list = None
) -> list:
    """
    Generate balanced and intelligent interview questions.

    Question categories:

    1. Resume Projects
    2. Matched Job Skills
    3. Missing Job Skills
    4. Resume-only Skills
    5. Job-specific Scenarios
    6. HR Questions

    For a 15-question interview, the target distribution is:

        Resume Projects       -> 3
        Matched Skills        -> 3
        Missing Skills        -> 2
        Resume-only Skills    -> 3
        Job Scenarios         -> 2
        HR Questions          -> 2

    Total = 15

    The function keeps skill matching case-insensitive
    and preserves the original skill order.
    """

    # ========================================================
    # SAFE DEFAULTS
    # ========================================================

    skills = skills or []
    resume_skills = resume_skills or []
    job_skills = job_skills or []

    resume_text = resume_text or ""
    job_description = job_description or ""

    # ========================================================
    # NORMALIZATION
    # ========================================================

    def normalize(value):
        return str(value).strip().lower()

    # ========================================================
    # KEEP ORIGINAL SKILL NAMES
    # ========================================================

    resume_skill_map = {}

    for skill in resume_skills:

        if not str(skill).strip():
            continue

        key = normalize(skill)

        if key not in resume_skill_map:
            resume_skill_map[key] = skill

    job_skill_map = {}

    for skill in job_skills:

        if not str(skill).strip():
            continue

        key = normalize(skill)

        if key not in job_skill_map:
            job_skill_map[key] = skill

    # ========================================================
    # FALLBACK
    # ========================================================

    if not resume_skill_map and skills:

        for skill in skills:

            if not str(skill).strip():
                continue

            key = normalize(skill)

            if key not in resume_skill_map:
                resume_skill_map[key] = skill

    # ========================================================
    # SKILL NAMES
    # ========================================================

    resume_skill_names = list(
        resume_skill_map.keys()
    )

    job_skill_names = list(
        job_skill_map.keys()
    )

    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    matched_skill_names = [
        skill
        for skill in resume_skill_names
        if skill in job_skill_map
    ]

    # ========================================================
    # MISSING JOB SKILLS
    # ========================================================

    missing_skill_names = [
        skill
        for skill in job_skill_names
        if skill not in resume_skill_map
    ]

    # ========================================================
    # RESUME-ONLY SKILLS
    # ========================================================

    resume_only_skill_names = [
        skill
        for skill in resume_skill_names
        if skill not in job_skill_map
    ]

    # ========================================================
    # ORIGINAL SKILL VALUES
    # ========================================================

    matched_skills = [
        resume_skill_map[name]
        for name in matched_skill_names
    ]

    missing_skills = [
        job_skill_map[name]
        for name in missing_skill_names
    ]

    resume_only_skills = [
        resume_skill_map[name]
        for name in resume_only_skill_names
    ]

    # ========================================================
    # QUESTION CATEGORY LISTS
    # ========================================================

    project_questions = []
    matched_questions = []
    missing_questions = []
    resume_skill_questions = []
    scenario_questions = []
    hr_questions = []

    # ========================================================
    # PROJECT EXTRACTION
    # ========================================================

    def extract_projects(text):

        if not text:
            return []

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        projects = []

        project_section = False
        current_project = None

        project_headers = [
            "projects",
            "project",
            "academic projects",
            "personal projects",
            "key projects"
        ]

        stop_sections = [
            "experience",
            "education",
            "certifications",
            "skills",
            "achievements",
            "interests",
            "languages",
            "publications",
            "coursework",
            "declaration",
            "technical skills",
            "professional experience"
        ]

        # ----------------------------------------------------
        # SAVE CURRENT PROJECT
        # ----------------------------------------------------

        def save_current_project():

            nonlocal current_project

            if current_project:

                cleaned_project = (
                    current_project.strip()
                )

                if (
                    len(cleaned_project) >= 4
                    and len(cleaned_project) <= 250
                ):
                    projects.append(
                        cleaned_project
                    )

            current_project = None

        # ----------------------------------------------------
        # PROCESS RESUME LINES
        # ----------------------------------------------------

        for line in lines:

            lower_line = line.lower().strip()

            # ------------------------------------------------
            # START PROJECT SECTION
            # ------------------------------------------------

            if any(
                lower_line == header
                or lower_line.startswith(
                    header + ":"
                )
                for header in project_headers
            ):

                save_current_project()

                project_section = True

                continue

            # ------------------------------------------------
            # STOP PROJECT SECTION
            # ------------------------------------------------

            if project_section:

                if any(
                    lower_line == section
                    or lower_line.startswith(
                        section + ":"
                    )
                    for section in stop_sections
                ):

                    save_current_project()

                    break

                # ------------------------------------------------
                # CLEAN BULLETS / NUMBERING
                # ------------------------------------------------

                cleaned = line.lstrip(
                    "•-*0123456789. "
                ).strip()

                if not cleaned:
                    continue

                # ------------------------------------------------
                # IGNORE VERY LONG PARAGRAPHS
                # ------------------------------------------------

                if len(cleaned) > 180:
                    continue

                # ------------------------------------------------
                # TECHNOLOGY SEPARATORS
                # ------------------------------------------------

                technology_separators = (
                    " — ",
                    " – ",
                    " - ",
                    " | "
                )

                looks_like_title = any(
                    separator in cleaned
                    for separator in technology_separators
                )

                # ------------------------------------------------
                # FIRST PROJECT
                # ------------------------------------------------

                if current_project is None:

                    current_project = cleaned

                    continue

                # ------------------------------------------------
                # NEW PROJECT TITLE
                # ------------------------------------------------

                if looks_like_title:

                    save_current_project()

                    current_project = cleaned

                    continue

                # ------------------------------------------------
                # DESCRIPTION
                # ------------------------------------------------

                # Description lines remain part of the
                # current project and are not treated
                # as separate projects.

                continue

        # ----------------------------------------------------
        # SAVE LAST PROJECT
        # ----------------------------------------------------

        save_current_project()

        # ----------------------------------------------------
        # REMOVE DUPLICATE PROJECTS
        # ----------------------------------------------------

        unique_projects = []

        seen_projects = set()

        for project in projects:

            project_key = normalize(
                project
            )

            if project_key in seen_projects:
                continue

            seen_projects.add(
                project_key
            )

            unique_projects.append(
                project
            )

        return unique_projects[:5]

    # ========================================================
    # EXTRACT PROJECTS
    # ========================================================

    projects = extract_projects(
        resume_text
    )

    # ========================================================
    # HELPER: FIND DATABASE SKILL
    # ========================================================

    def find_database_skill(skill_name):

        normalized_skill = normalize(
            skill_name
        )

        for database_skill in QUESTIONS:

            if normalize(
                database_skill
            ) == normalized_skill:

                return database_skill

        return None

    # ========================================================
    # 1. RESUME PROJECT QUESTIONS
    # ========================================================

    for project in projects:

        project_questions.append({

            "skill": "Resume Project",

            "type": "Project",

            "difficulty": "Medium",

            "question": (
                f"Explain the project "
                f"'{project}' mentioned in your resume. "
                f"What problem did it solve, what was "
                f"your role, what technologies did you "
                f"use, and what was the main outcome?"
            ),

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        })

        # Maximum 5 project candidates
        if len(project_questions) >= 5:
            break

    # ========================================================
    # CUSTOM INTELLIGENT MATCHED QUESTIONS
    # ========================================================

    matched_question_templates = {

        "python": [
            (
                "How did you use Python in your projects? "
                "Explain an important Python feature, library, "
                "or implementation decision you used."
            ),
            (
                "How would you design a maintainable Python "
                "backend application with proper error handling "
                "and reusable components?"
            )
        ],

        "fastapi": [
            (
                "How did you use FastAPI in your projects? "
                "Explain how you designed an API endpoint and "
                "handled request validation and responses."
            ),
            (
                "How would you secure and structure a "
                "production FastAPI application?"
            )
        ],

        "react": [
            (
                "How did you use React in your projects? "
                "Explain how components, state, and API "
                "communication were handled."
            )
        ],

        "postgresql": [
            (
                "How would you use PostgreSQL with a FastAPI "
                "application? Explain the database connection, "
                "tables, queries, and API interaction."
            )
        ],

        "sql": [
            (
                "How have you used SQL in your projects? "
                "Explain a database operation or query you "
                "implemented and why."
            )
        ],

        "javascript": [
            (
                "How did you use JavaScript in your projects? "
                "Explain how JavaScript interacted with the "
                "frontend or backend."
            )
        ],

        "machine learning": [
            (
                "Describe a machine learning project you worked "
                "on. Which algorithm did you use, why did you "
                "choose it, and how did you evaluate the model?"
            )
        ],

        "deep learning": [
            (
                "Describe a deep learning project you worked on. "
                "What architecture or model did you use and why?"
            )
        ],

        "computer vision": [
            (
                "Describe a computer vision problem you solved. "
                "What model, preprocessing, or detection approach "
                "did you use?"
            )
        ],

        "nlp": [
            (
                "Describe an NLP problem you worked on. "
                "How did you preprocess the text and what "
                "techniques did you use?"
            )
        ],

        "tensorflow": [
            (
                "How have you used TensorFlow in your projects? "
                "Explain the model-building, training, or "
                "deployment process."
            )
        ],

        "pytorch": [
            (
                "How have you used PyTorch in your projects? "
                "Explain the model, training process, or "
                "implementation you worked on."
            )
        ],

        "scikit-learn": [
            (
                "How have you used Scikit-learn in a machine "
                "learning project? Explain preprocessing, "
                "training, and evaluation."
            )
        ],

        "git": [
            (
                "How have you used Git while developing your "
                "projects? Explain a Git workflow you followed."
            )
        ],

        "github": [
            (
                "How have you used GitHub for version control, "
                "project collaboration, or code management?"
            )
        ]
    }

    # ========================================================
    # 2. MATCHED SKILL QUESTIONS
    # ========================================================

    for skill_name in matched_skill_names:

        skill = resume_skill_map[
            skill_name
        ]

        question_added = False

        # ----------------------------------------------------
        # CUSTOM QUESTION
        # ----------------------------------------------------

        if skill_name in matched_question_templates:

            question_text = (
                matched_question_templates[
                    skill_name
                ][0]
            )

            matched_questions.append({

                "skill": skill,

                "type": "Matched Skill",

                "difficulty": "Hard",

                "question": question_text,

                "time_limit": (
                    INTERVIEW_TIME_LIMITS[
                        "Hard"
                    ]
                )
            })

            question_added = True

        # ----------------------------------------------------
        # DATABASE FALLBACK
        # ----------------------------------------------------

        if not question_added:

            database_skill = find_database_skill(
                skill_name
            )

            if database_skill:

                skill_questions = QUESTIONS[
                    database_skill
                ]

                advanced_questions = (
                    skill_questions.get(
                        "advanced",
                        []
                    )
                )

                technical_questions = (
                    skill_questions.get(
                        "technical",
                        []
                    )
                )

                if advanced_questions:

                    question_text = (
                        advanced_questions[0]
                    )

                    difficulty = "Hard"

                elif technical_questions:

                    question_text = (
                        technical_questions[0]
                    )

                    difficulty = "Medium"

                else:

                    question_text = (
                        f"Explain how your experience "
                        f"with {skill} matches the "
                        f"requirements of this job."
                    )

                    difficulty = "Medium"

                matched_questions.append({

                    "skill": skill,

                    "type": "Matched Skill",

                    "difficulty": difficulty,

                    "question": question_text,

                    "time_limit": (
                        INTERVIEW_TIME_LIMITS[
                            difficulty
                        ]
                    )
                })

            else:

                matched_questions.append({

                    "skill": skill,

                    "type": "Matched Skill",

                    "difficulty": "Medium",

                    "question": (
                        f"Explain how your experience "
                        f"with {skill} matches the "
                        f"requirements of this job."
                    ),

                    "time_limit": (
                        INTERVIEW_TIME_LIMITS[
                            "Medium"
                        ]
                    )
                })

    # ========================================================
    # MISSING JOB SKILL QUESTIONS
    # ========================================================

    missing_question_templates = {

        "postgresql": (
            "You have mentioned SQL in your resume, but "
            "PostgreSQL is required for this role. What is "
            "PostgreSQL, how is it different from SQL, and "
            "how would you use PostgreSQL with FastAPI?"
        ),

        "fastapi": (
            "FastAPI is required for this role. Explain how "
            "you would build a REST API using FastAPI, including "
            "request validation and error handling."
        ),

        "python": (
            "Python is required for this role. Explain how "
            "you would structure a maintainable Python backend "
            "application."
        ),

        "sql": (
            "SQL is required for this role. Explain how you "
            "would retrieve, insert, update, and filter data "
            "in a relational database."
        ),

        "javascript": (
            "JavaScript is required for this role. Explain "
            "how you would use JavaScript to communicate "
            "with a backend API."
        ),

        "react": (
            "React is required for this role. Explain how "
            "you would build a frontend using reusable "
            "components and manage application state."
        ),

        "docker": (
            "Docker is required for this role. Explain how "
            "you would containerize and deploy a FastAPI "
            "application using Docker."
        ),

        "aws": (
            "AWS is required for this role. Explain how "
            "you would deploy a backend application on AWS "
            "and what services you would consider."
        )
    }

    # ========================================================
    # 3. MISSING JOB SKILLS
    # ========================================================

    for skill_name in missing_skill_names:

        skill = job_skill_map[
            skill_name
        ]

        question_text = (
            missing_question_templates.get(
                skill_name
            )
        )

        if question_text is None:

            database_skill = find_database_skill(
                skill_name
            )

            if database_skill:

                skill_questions = QUESTIONS[
                    database_skill
                ]

                technical_questions = (
                    skill_questions.get(
                        "technical",
                        []
                    )
                )

                if technical_questions:

                    question_text = (
                        technical_questions[0]
                    )

            if question_text is None:

                question_text = (
                    f"This role requires {skill}. "
                    f"What do you know about {skill}, "
                    f"and how would you use it in a "
                    f"real-world project?"
                )

        missing_questions.append({

            "skill": skill,

            "type": "Job Requirement",

            "difficulty": "Medium",

            "question": question_text,

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        })

    # ========================================================
    # RESUME-ONLY SKILL QUESTIONS
    # ========================================================

    resume_skill_templates = {

        "c": (
            "You have listed C on your resume. Describe a "
            "program or academic problem where you used C "
            "and explain the concepts you applied."
        ),

        "javascript": (
            "You have listed JavaScript on your resume. "
            "Describe how you used JavaScript in one of "
            "your projects."
        ),

        "html": (
            "You have listed HTML on your resume. Explain "
            "how you structured the frontend of one of "
            "your projects."
        ),

        "css": (
            "You have listed CSS on your resume. Explain "
            "how you designed or styled one of your projects."
        ),

        "artificial intelligence": (
            "You have listed Artificial Intelligence on your "
            "resume. Describe an AI problem you worked on "
            "and the approach you used."
        ),

        "machine learning": (
            "Describe a machine learning project from your "
            "resume. What data did you use, what model did "
            "you select, and how did you evaluate it?"
        ),

        "deep learning": (
            "Describe a deep learning project you worked on. "
            "What architecture or model did you use and why?"
        ),

        "nlp": (
            "Describe an NLP task you worked on and explain "
            "how you processed the text data."
        ),

        "computer vision": (
            "Describe a computer vision project from your "
            "resume and explain the main technical challenges."
        ),

        "tensorflow": (
            "Describe how you used TensorFlow in a project "
            "and explain the model training process."
        ),

        "pytorch": (
            "Describe how you used PyTorch in a project and "
            "explain an important implementation decision."
        ),

        "scikit-learn": (
            "Describe how you used Scikit-learn in a machine "
            "learning project and explain the preprocessing "
            "and evaluation steps."
        ),

        "git": (
            "How have you used Git while working on your "
            "projects? Explain a Git workflow you followed."
        ),

        "github": (
            "How have you used GitHub for project development, "
            "version control, or collaboration?"
        )
    }

    # ========================================================
    # 4. RESUME-ONLY SKILLS
    # ========================================================

    for skill_name in resume_only_skill_names:

        skill = resume_skill_map[
            skill_name
        ]

        question_text = (
            resume_skill_templates.get(
                skill_name
            )
        )

        if question_text is None:

            database_skill = find_database_skill(
                skill_name
            )

            if database_skill:

                skill_questions = QUESTIONS[
                    database_skill
                ]

                technical_questions = (
                    skill_questions.get(
                        "technical",
                        []
                    )
                )

                if technical_questions:

                    question_text = (
                        technical_questions[0]
                    )

            if question_text is None:

                question_text = (
                    f"How have you used {skill} "
                    f"in your projects, academic "
                    f"work, or previous experience?"
                )

        resume_skill_questions.append({

            "skill": skill,

            "type": "Resume Skill",

            "difficulty": "Medium",

            "question": question_text,

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        })

    # ========================================================
    # 5. JOB-SPECIFIC SCENARIO QUESTIONS
    # ========================================================

    if job_description:

        # ----------------------------------------------------
        # PYTHON + FASTAPI
        # ----------------------------------------------------

        if (
            "python" in job_skill_map
            and "fastapi" in job_skill_map
        ):

            scenario_questions.append({

                "skill": "Python, FastAPI",

                "type": "Scenario",

                "difficulty": "Hard",

                "question": (
                    "Suppose you are asked to build a backend "
                    "service using Python and FastAPI. How would "
                    "you design the API, validate incoming data, "
                    "handle errors, and structure the application?"
                ),

                "time_limit": (
                    INTERVIEW_TIME_LIMITS[
                        "Hard"
                    ]
                )
            })

        # ----------------------------------------------------
        # FASTAPI + POSTGRESQL
        # ----------------------------------------------------

        if (
            "fastapi" in job_skill_map
            and "postgresql" in job_skill_map
        ):

            scenario_questions.append({

                "skill": "FastAPI, PostgreSQL",

                "type": "Scenario",

                "difficulty": "Hard",

                "question": (
                    "Suppose you need to build a FastAPI "
                    "application with PostgreSQL. How would "
                    "you connect the API to the database and "
                    "design the interaction between API "
                    "endpoints and database tables?"
                ),

                "time_limit": (
                    INTERVIEW_TIME_LIMITS[
                        "Hard"
                    ]
                )
            })

        # ----------------------------------------------------
        # MACHINE LEARNING + PYTHON
        # ----------------------------------------------------

        if (
            "machine learning" in job_skill_map
            and "python" in job_skill_map
        ):

            scenario_questions.append({

                "skill": "Python, Machine Learning",

                "type": "Scenario",

                "difficulty": "Hard",

                "question": (
                    "Suppose you receive a new machine learning "
                    "dataset for this role. Explain how you would "
                    "use Python to preprocess the data, train a "
                    "model, evaluate it, and prepare it for use "
                    "in an application."
                ),

                "time_limit": (
                    INTERVIEW_TIME_LIMITS[
                        "Hard"
                    ]
                )
            })

        # ----------------------------------------------------
        # GENERIC SCENARIO
        # ----------------------------------------------------

        primary_skill = None

        if matched_skills:

            primary_skill = matched_skills[0]

        elif job_skills:

            primary_skill = job_skills[0]

        elif resume_skills:

            primary_skill = resume_skills[0]

        if primary_skill:

            scenario_questions.append({

                "skill": "Job Scenario",

                "type": "Scenario",

                "difficulty": "Hard",

                "question": (
                    f"Based on the job requirements, "
                    f"how would you use {primary_skill} "
                    f"to solve a real-world problem "
                    f"in this role?"
                ),

                "time_limit": (
                    INTERVIEW_TIME_LIMITS[
                        "Hard"
                    ]
                )
            })

    # ========================================================
    # 6. HR QUESTIONS
    # ========================================================

    personalized_hr = [

        {
            "question": (
                "Tell me about yourself and explain "
                "how your background matches this job."
            ),
            "difficulty": "Easy"
        },

        {
            "question": (
                "Why are you interested in this role, "
                "and how does your experience match "
                "the job description?"
            ),
            "difficulty": "Easy"
        },

        {
            "question": (
                "Which project from your resume best "
                "demonstrates your suitability for "
                "this position?"
            ),
            "difficulty": "Medium"
        },

        {
            "question": (
                "What technical skill are you currently "
                "working to improve, and why?"
            ),
            "difficulty": "Easy"
        }
    ]

    for item in personalized_hr:

        difficulty = item[
            "difficulty"
        ]

        hr_questions.append({

            "skill": "General",

            "type": "HR",

            "difficulty": difficulty,

            "question": item[
                "question"
            ],

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    difficulty
                ]
            )
        })

    # ========================================================
    # REMOVE DUPLICATE QUESTIONS
    # ========================================================

    def deduplicate_questions(question_list):

        unique = []
        seen = set()

        for item in question_list:

            question_text = (
                item.get(
                    "question",
                    ""
                )
                .strip()
                .lower()
            )

            if not question_text:
                continue

            if question_text in seen:
                continue

            seen.add(
                question_text
            )

            unique.append(
                item
            )

        return unique

    project_questions = deduplicate_questions(
        project_questions
    )

    matched_questions = deduplicate_questions(
        matched_questions
    )

    missing_questions = deduplicate_questions(
        missing_questions
    )

    resume_skill_questions = deduplicate_questions(
        resume_skill_questions
    )

    scenario_questions = deduplicate_questions(
        scenario_questions
    )

    hr_questions = deduplicate_questions(
        hr_questions
    )

    # ========================================================
    # BALANCED SELECTION
    # ========================================================

    selected_questions = []
    selected_question_keys = set()

    def add_category_questions(
        question_list,
        target_count
    ):
        """
        Add up to target_count questions from one category.
        Duplicate questions are skipped.
        """

        added = 0

        for item in question_list:

            if added >= target_count:
                break

            question_key = (
                item.get(
                    "question",
                    ""
                )
                .strip()
                .lower()
            )

            if not question_key:
                continue

            if question_key in selected_question_keys:
                continue

            selected_questions.append(
                item
            )

            selected_question_keys.add(
                question_key
            )

            added += 1

    # ========================================================
    # TARGET DISTRIBUTION
    # ========================================================

    # 3 Resume Projects
    add_category_questions(
        project_questions,
        3
    )

    # 3 Matched Job Skills
    add_category_questions(
        matched_questions,
        3
    )

    # 2 Missing Job Skills
    add_category_questions(
        missing_questions,
        2
    )

    # 3 Resume-only Skills
    add_category_questions(
        resume_skill_questions,
        3
    )

    # 2 Job Scenarios
    add_category_questions(
        scenario_questions,
        2
    )

    # 2 HR Questions
    add_category_questions(
        hr_questions,
        2
    )

    # ========================================================
    # FILL REMAINING QUESTIONS
    # ========================================================

    if len(selected_questions) < number_of_questions:

        remaining_categories = [

            project_questions,
            matched_questions,
            missing_questions,
            resume_skill_questions,
            scenario_questions,
            hr_questions
        ]

        for category in remaining_categories:

            if len(selected_questions) >= number_of_questions:
                break

            for item in category:

                if len(selected_questions) >= number_of_questions:
                    break

                question_key = (
                    item.get(
                        "question",
                        ""
                    )
                    .strip()
                    .lower()
                )

                if not question_key:
                    continue

                if question_key in selected_question_keys:
                    continue

                selected_questions.append(
                    item
                )

                selected_question_keys.add(
                    question_key
                )

    # ========================================================
    # FINAL FALLBACK QUESTIONS
    # ========================================================

    fallback_questions = [

        {
            "skill": "General",

            "type": "Technical",

            "difficulty": "Medium",

            "question": (
                "Describe a difficult technical problem "
                "you solved and explain your approach."
            ),

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        },

        {
            "skill": "General",

            "type": "Technical",

            "difficulty": "Medium",

            "question": (
                "How do you debug an application when "
                "the expected result is not produced?"
            ),

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        },

        {
            "skill": "General",

            "type": "Technical",

            "difficulty": "Medium",

            "question": (
                "How do you make sure your code is reliable, "
                "maintainable, and easy for other developers "
                "to understand?"
            ),

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Medium"
                ]
            )
        },

        {
            "skill": "General",

            "type": "HR",

            "difficulty": "Easy",

            "question": (
                "Tell me about yourself."
            ),

            "time_limit": (
                INTERVIEW_TIME_LIMITS[
                    "Easy"
                ]
            )
        }
    ]

    # ========================================================
    # ADD FALLBACK ONLY IF REQUIRED
    # ========================================================

    for item in fallback_questions:

        if len(selected_questions) >= number_of_questions:
            break

        question_key = (
            item.get(
                "question",
                ""
            )
            .strip()
            .lower()
        )

        if question_key in selected_question_keys:
            continue

        selected_questions.append(
            item
        )

        selected_question_keys.add(
            question_key
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return selected_questions[
        :number_of_questions
    ]

# ============================================================
# QUESTION TOPIC DATABASE
# ============================================================

QUESTION_TOPICS = {

    "python": [
        "python",
        "list",
        "tuple",
        "set",
        "decorator",
        "generator",
        "exception",
        "multiprocessing",
        "multithreading",
        "memory management",
        "object oriented",
        "oop"
    ],

    "fastapi": [
        "fastapi",
        "dependency injection",
        "rest api",
        "jwt",
        "authentication",
        "authorization",
        "endpoint",
        "api",
        "high traffic"
    ],

    "react": [
        "react",
        "component",
        "components",
        "hooks",
        "props",
        "state",
        "virtual dom",
        "useeffect",
        "usememo"
    ],

    "postgresql": [
        "postgresql",
        "sql",
        "primary key",
        "foreign key",
        "database",
        "indexing",
        "normalization",
        "query"
    ],

    "machine learning": [
        "machine learning",
        "supervised",
        "unsupervised",
        "overfitting",
        "classification",
        "regression",
        "bias",
        "variance",
        "imbalanced",
        "features"
    ],

    "deep learning": [
        "deep learning",
        "neural network",
        "activation function",
        "backpropagation",
        "gradient",
        "cnn",
        "rnn",
        "transformer"
    ],

    "nlp": [
        "nlp",
        "natural language",
        "tokenization",
        "token",
        "embedding",
        "stemming",
        "lemmatization",
        "transformer",
        "attention",
        "bert"
    ],

    "tensorflow": [
        "tensorflow",
        "keras",
        "neural network",
        "overfitting",
        "model",
        "deploy"
    ],

    "pytorch": [
        "pytorch",
        "tensor",
        "autograd",
        "automatic differentiation",
        "backpropagation",
        "train",
        "model"
    ],

    "git": [
        "git",
        "github",
        "branch",
        "merge",
        "merge conflict",
        "rebase",
        "commit"
    ],

    "docker": [
        "docker",
        "container",
        "image",
        "dockerfile",
        "deployment",
        "portable"
    ],

    "aws": [
        "aws",
        "amazon",
        "ec2",
        "s3",
        "cloud",
        "serverless",
        "deployment"
    ]
}


# ============================================================
# GET EXPECTED CONCEPTS FOR QUESTION
# ============================================================

def get_expected_concepts(question: str) -> list:

    question_lower = (
        question or ""
    ).strip().lower()

    expected = []

    # ========================================================
    # PYTHON
    # ========================================================

    if "main features of python" in question_lower:

        expected = [
            "high-level",
            "interpreted",
            "dynamically typed",
            "object-oriented",
            "readable",
            "large standard library",
            "cross-platform"
        ]

    elif (
        "list, tuple and set"
        in question_lower
    ):

        expected = [
            "list",
            "mutable",
            "ordered",
            "tuple",
            "immutable",
            "set",
            "unique",
            "unordered"
        ]

    elif (
        "object-oriented programming"
        in question_lower
    ):

        expected = [
            "class",
            "object",
            "inheritance",
            "encapsulation",
            "polymorphism",
            "abstraction"
        ]

    elif "exception handling" in question_lower:

        expected = [
            "try",
            "except",
            "finally",
            "raise",
            "error",
            "exception"
        ]

    elif "decorators and generators" in question_lower:

        expected = [
            "decorator",
            "function",
            "wrapper",
            "generator",
            "yield",
            "lazy"
        ]

    elif "python memory management" in question_lower:

        expected = [
            "memory",
            "heap",
            "garbage collection",
            "reference",
            "object"
        ]

    elif (
        "multiprocessing and multithreading"
        in question_lower
    ):

        expected = [
            "multiprocessing",
            "multithreading",
            "process",
            "thread",
            "cpu",
            "gil",
            "parallel"
        ]

        # ========================================================
    # FASTAPI
    # ========================================================

    elif (
        "why would you use fastapi" in question_lower
        or "why use fastapi" in question_lower
        or "traditional python web framework" in question_lower
        or (
            "what is fastapi" in question_lower
            and (
                "why would you use it" in question_lower
                or "why use it" in question_lower
                or "why do you use it" in question_lower
            )
        )
    ):

        expected = [
            "fastapi",
            "python",
            "web framework",
            "api",
            "asynchronous",
            "async",
            "high performance",
            "performance",
            "automatic documentation",
            "swagger",
            "openapi",
            "validation",
            "pydantic"
        ]

    elif question_lower == "what is fastapi?":

        expected = [
            "fastapi",
            "python",
            "web framework",
            "api",
            "rest api",
            "asynchronous",
            "async",
            "high performance",
            "performance"
        ]

    elif "dependency injection in fastapi" in question_lower:

        expected = [
            "dependency",
            "inject",
            "depends",
            "reusable",
            "dependency injection"
        ]

    elif (
        "rest api" in question_lower
        and "fastapi" in question_lower
        and not is_scenario_question
    ):

        expected = [
            "endpoint",
            "get",
            "post",
            "put",
            "delete",
            "http",
            "request",
            "response"
        ]

    elif "secure a fastapi" in question_lower:

        expected = [
            "authentication",
            "authorization",
            "jwt",
            "https",
            "validation",
            "security"
        ]

    elif "jwt" in question_lower:

        expected = [
            "jwt",
            "token",
            "authentication",
            "authorization",
            "access token",
            "secret"
        ]

    elif "high traffic" in question_lower:

        expected = [
            "async",
            "asynchronous",
            "caching",
            "database",
            "connection pooling",
            "load balancing",
            "scaling"
        ]

    # ========================================================
    # REACT
    # ========================================================

    elif question_lower == "what is react?":

        expected = [
            "javascript",
            "library",
            "user interface",
            "component",
            "frontend"
        ]

    elif "react components" in question_lower:

        expected = [
            "component",
            "reusable",
            "ui",
            "props",
            "state"
        ]

    elif "react hooks" in question_lower:

        expected = [
            "hooks",
            "usestate",
            "useeffect",
            "functional component",
            "state",
            "lifecycle"
        ]

    elif "props and state" in question_lower:

        expected = [
            "props",
            "state",
            "immutable",
            "component",
            "data"
        ]

    elif "virtual dom" in question_lower:

        expected = [
            "virtual dom",
            "dom",
            "diff",
            "reconciliation",
            "performance",
            "javascript object"
        ]

    elif "optimize a react" in question_lower:

        expected = [
            "memoization",
            "usememo",
            "usecallback",
            "lazy loading",
            "code splitting",
            "virtual dom"
        ]

    elif "useeffect and usememo" in question_lower:

        expected = [
            "useeffect",
            "side effect",
            "usememo",
            "memoization",
            "dependency"
        ]

    # ========================================================
    # POSTGRESQL
    # ========================================================

    elif question_lower == "what is postgresql?":

        expected = [
            "database",
            "relational",
            "sql",
            "open source",
            "postgresql"
        ]

    elif "primary key" in question_lower:

        expected = [
            "unique",
            "identify",
            "row",
            "record",
            "not null"
        ]

    elif "foreign key" in question_lower:

        expected = [
            "relationship",
            "table",
            "reference",
            "primary key"
        ]

    elif "sql and nosql" in question_lower:

        expected = [
            "sql",
            "relational",
            "structured",
            "nosql",
            "non relational",
            "schema"
        ]

    elif "database indexing" in question_lower:

        expected = [
            "index",
            "search",
            "query",
            "performance",
            "database"
        ]

    elif "slow postgresql query" in question_lower:

        expected = [
            "index",
            "query plan",
            "explain",
            "optimize",
            "database"
        ]

    elif "database normalization" in question_lower:

        expected = [
            "normalization",
            "redundancy",
            "data integrity",
            "tables",
            "normal forms"
        ]

    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    elif question_lower == "what is machine learning?":

        expected = [
            "machine learning",
            "data",
            "algorithm",
            "learn",
            "prediction",
            "pattern"
        ]

    elif (
        "supervised and unsupervised"
        in question_lower
    ):

        expected = [
            "supervised",
            "labeled",
            "unsupervised",
            "unlabeled",
            "data"
        ]

    elif "overfitting" in question_lower:

        expected = [
            "training data",
            "test data",
            "generalization",
            "complex model",
            "regularization"
        ]

    elif (
        "classification and regression"
        in question_lower
    ):

        expected = [
            "classification",
            "categorical",
            "class",
            "regression",
            "continuous",
            "numeric"
        ]

    elif "bias-variance" in question_lower:

        expected = [
            "bias",
            "variance",
            "underfitting",
            "overfitting",
            "generalization"
        ]

    elif "imbalanced dataset" in question_lower:

        expected = [
            "imbalanced",
            "oversampling",
            "undersampling",
            "smote",
            "class weights"
        ]

    elif "best features" in question_lower:

        expected = [
            "feature selection",
            "correlation",
            "importance",
            "model",
            "dimensionality"
        ]

    # ========================================================
    # DEEP LEARNING
    # ========================================================

    elif question_lower == "what is deep learning?":

        expected = [
            "neural network",
            "deep",
            "layers",
            "machine learning",
            "data"
        ]

    elif "artificial neural network" in question_lower:

        expected = [
            "neuron",
            "input",
            "weight",
            "bias",
            "activation",
            "layers"
        ]

    elif "activation function" in question_lower:

        expected = [
            "activation",
            "nonlinear",
            "relu",
            "sigmoid",
            "output"
        ]

    elif "backpropagation" in question_lower:

        expected = [
            "gradient",
            "error",
            "loss",
            "backward",
            "weights",
            "update"
        ]

    elif "vanishing and exploding" in question_lower:

        expected = [
            "gradient",
            "vanishing",
            "exploding",
            "deep network",
            "activation",
            "normalization"
        ]

    elif "cnn and rnn" in question_lower:

        expected = [
            "cnn",
            "convolution",
            "image",
            "rnn",
            "sequence",
            "recurrent"
        ]

    elif "transformers useful" in question_lower:

        expected = [
            "transformer",
            "attention",
            "parallel",
            "sequence",
            "nlp"
        ]

    # ========================================================
    # NLP
    # ========================================================

    elif (
        "natural language processing"
        in question_lower
    ):

        expected = [
            "language",
            "text",
            "human language",
            "nlp",
            "machine learning"
        ]

    elif "tokenization" in question_lower:

        expected = [
            "token",
            "text",
            "words",
            "sentences",
            "split"
        ]

    elif "word embeddings" in question_lower:

        expected = [
            "vector",
            "word",
            "semantic",
            "meaning",
            "embedding"
        ]

    elif "stemming and lemmatization" in question_lower:

        expected = [
            "stemming",
            "lemmatization",
            "root",
            "word",
            "dictionary"
        ]

    elif "transformer models" in question_lower:

        expected = [
            "transformer",
            "attention",
            "encoder",
            "decoder",
            "sequence"
        ]

    elif "attention work in nlp" in question_lower:

        expected = [
            "attention",
            "query",
            "key",
            "value",
            "weights",
            "context"
        ]

    elif "bert" in question_lower:

        expected = [
            "bert",
            "transformer",
            "context",
            "bidirectional",
            "pretrained",
            "embedding"
        ]

    # ========================================================
    # TENSORFLOW
    # ========================================================

    elif question_lower == "what is tensorflow?":

        expected = [
            "machine learning",
            "deep learning",
            "framework",
            "tensor",
            "neural network"
        ]

    elif "what is keras" in question_lower:

        expected = [
            "keras",
            "deep learning",
            "neural network",
            "tensorflow",
            "api"
        ]

    elif "neural network using tensorflow" in question_lower:

        expected = [
            "tensorflow",
            "keras",
            "model",
            "layer",
            "compile",
            "train"
        ]

    elif "prevent overfitting in a tensorflow" in question_lower:

        expected = [
            "dropout",
            "regularization",
            "early stopping",
            "data augmentation",
            "overfitting"
        ]

    # ========================================================
    # PYTORCH
    # ========================================================

    elif question_lower == "what is pytorch?":

        expected = [
            "machine learning",
            "deep learning",
            "framework",
            "tensor",
            "neural network"
        ]

    elif "what is a tensor" in question_lower:

        expected = [
            "tensor",
            "multidimensional",
            "array",
            "data",
            "pytorch"
        ]

    elif "autograd" in question_lower:

        expected = [
            "autograd",
            "gradient",
            "automatic differentiation",
            "backpropagation"
        ]

    elif "automatic differentiation" in question_lower:

        expected = [
            "automatic differentiation",
            "gradient",
            "autograd",
            "computational graph",
            "backpropagation"
        ]

    # ========================================================
    # GIT
    # ========================================================

    elif question_lower == "what is git?":

        expected = [
            "version control",
            "repository",
            "code",
            "commit",
            "history"
        ]

    elif "git and github" in question_lower:

        expected = [
            "git",
            "github",
            "version control",
            "repository",
            "remote"
        ]

    elif "git branch" in question_lower:

        expected = [
            "branch",
            "version",
            "development",
            "commit",
            "code"
        ]

    elif "merge conflict" in question_lower:

        expected = [
            "conflict",
            "merge",
            "branch",
            "resolve",
            "changes"
        ]

    elif "git rebase" in question_lower:

        expected = [
            "rebase",
            "commit",
            "history",
            "branch",
            "linear"
        ]

    elif "merge and rebase" in question_lower:

        expected = [
            "merge",
            "rebase",
            "commit",
            "history",
            "branch"
        ]

    # ========================================================
    # DOCKER
    # ========================================================

    elif question_lower == "what is docker?":

        expected = [
            "container",
            "application",
            "dependencies",
            "image",
            "deployment"
        ]

    elif "docker container" in question_lower:

        expected = [
            "container",
            "isolated",
            "application",
            "image",
            "environment"
        ]

    elif "docker image" in question_lower:

        expected = [
            "image",
            "template",
            "container",
            "application",
            "dependencies"
        ]

    elif "docker useful for deployment" in question_lower:

        expected = [
            "container",
            "deployment",
            "portable",
            "environment",
            "dependencies"
        ]

    elif "docker image and container" in question_lower:

        expected = [
            "image",
            "container",
            "template",
            "running",
            "application"
        ]

    elif "dockerize a fastapi" in question_lower:

        expected = [
            "dockerfile",
            "python",
            "fastapi",
            "image",
            "container",
            "port"
        ]

    # ========================================================
    # AWS
    # ========================================================

    elif question_lower == "what is aws?":

        expected = [
            "cloud",
            "aws",
            "services",
            "infrastructure",
            "amazon"
        ]

    elif "amazon ec2" in question_lower:

        expected = [
            "ec2",
            "virtual server",
            "compute",
            "cloud",
            "instance"
        ]

    elif "amazon s3" in question_lower:

        expected = [
            "s3",
            "storage",
            "object storage",
            "bucket",
            "cloud"
        ]

    elif "cloud deployment" in question_lower:

        expected = [
            "cloud",
            "deployment",
            "scalability",
            "infrastructure",
            "availability"
        ]

    elif "deploy a fastapi application on aws" in question_lower:

        expected = [
            "fastapi",
            "aws",
            "ec2",
            "server",
            "deployment",
            "security"
        ]

    elif "secure an aws application" in question_lower:

        expected = [
            "iam",
            "authentication",
            "authorization",
            "security",
            "encryption",
            "least privilege"
        ]

    elif "ec2 and serverless" in question_lower:

        expected = [
            "ec2",
            "server",
            "serverless",
            "lambda",
            "managed",
            "scaling"
        ]

    return expected


# ============================================================
# DETECT QUESTION TOPICS
# ============================================================

def detect_question_topics(question: str) -> list:

    question_lower = (
        question or ""
    ).lower()

    detected = []

    for topic, keywords in QUESTION_TOPICS.items():

        for keyword in keywords:

            if keyword in question_lower:

                detected.append(topic)

                break

    return list(
        dict.fromkeys(detected)
    )


# ============================================================
# STRICT QUESTION-AWARE INTERVIEW ANSWER EVALUATOR
# ============================================================

def evaluate_interview_answer(
    question: str,
    answer: str,
    job_description: str,
    time_taken: int,
    time_limit: int = 90
) -> dict:

    question = (question or "").strip()
    answer = (answer or "").strip()
    job_description = (job_description or "").strip()

    # ========================================================
    # BASIC NORMALIZATION
    # ========================================================

    question_lower = question.lower()
    answer_lower = answer.lower()

    answer_clean = re.sub(
        r"[^a-z0-9\s+#.-]",
        " ",
        answer_lower
    )

    answer_clean = re.sub(
        r"\s+",
        " ",
        answer_clean
    ).strip()

    word_count = len(answer.split())

    safe_time_limit = max(
        int(time_limit or 90),
        1
    )

    safe_time_taken = max(
        int(time_taken or 0),
        0
    )

    # ========================================================
    # EMPTY ANSWER
    # ========================================================

    if not answer:

        return {
            "score": 0,
            "overall_score": 0,
            "technical_score": 0,
            "project_score": 0,
            "communication_score": 0,
            "time_score": 0,
            "relevance_score": 0,
            "is_relevant": False,

            "feedback":
                "No answer was provided.",

            "strengths": [],

            "improvements": [
                "Provide an answer to the question.",
                "Explain the main concept clearly.",
                "Use a relevant example where possible."
            ],

            "matched_topics": [],
            "project_topics": [],

            "word_count": 0,
            "time_taken": safe_time_taken,
            "time_limit": safe_time_limit
        }

    # ========================================================
    # QUESTION TYPE DETECTION
    # ========================================================

    def contains_any(text, words):
        return any(
            word in text
            for word in words
        )

    # --------------------------------------------------------
    # PROJECT QUESTION
    # --------------------------------------------------------

  

    is_project_question = contains_any(
        question_lower,
        [
            "explain the project",
            "describe the project",
            "explain your project",
            "describe your project",
            "your project",
            "project from your resume",
            "project mentioned in your resume",
            "one of your projects",
            "your projects",
            "what was your role",
            "what problem did it solve",
            "main outcome"
        ]
    )

    # Handle questions where words appear between
    # "your" and "project"
    # Example:
    # "Explain your mental health prediction project."

    if (
        "explain" in question_lower
        and "project" in question_lower
        and "your" in question_lower
    ):
        is_project_question = True

    # --------------------------------------------------------
    # SCENARIO QUESTION
    # --------------------------------------------------------

    is_scenario_question = contains_any(
        question_lower,
        [
            "suppose you",
            "imagine you",
            "scenario",
            "how would you design",
            "how would you build",
            "how would you handle",
            "how would you implement",
            "how would you deploy",
            "how would you solve",
            "what would you do"
        ]
    )

    # --------------------------------------------------------
    # HR QUESTION
    # --------------------------------------------------------

    is_hr_question = contains_any(
        question_lower,
        [
            "tell me about yourself",
            "why are you interested",
            "why do you want",
            "why should we hire",
            "strength",
            "weakness",
            "where do you see yourself",
            "career goal",
            "team",
            "leadership",
            "conflict",
            "challenge"
        ]
    )
    # --------------------------------------------------------
    # BEHAVIORAL / SCENARIO QUESTION
    # --------------------------------------------------------

    is_behavioral_question = contains_any(
        question_lower,
        [
            "tell me about a challenging situation",
            "tell me about a challenge",
            "challenging situation",
            "how did you solve",
            "how did you handle",
            "describe a situation",
            "describe a time",
            "tell me about a time",
            "difficult situation",
            "problem you faced",
            "problem you solved",
            "how did you overcome",
            "how did you deal with",
            "situation you faced",
            "conflict you faced"
        ]
    )

    # Behavioral questions are more specific than broad HR terms
    # such as "challenge" or "conflict".
    if is_behavioral_question:
        is_hr_question = False

    # ========================================================
    # REQUIRED CONCEPTS
    # ========================================================
    #
    # Each question gets a group of concept requirements.
    #
    # IMPORTANT:
    # A technology name by itself does NOT count as
    # a complete answer.
    # ========================================================

    concept_groups = []

    # ========================================================
    # PYTHON
    # ========================================================

    if "main features of python" in question_lower:

        concept_groups = [
            ["programming language"],
            ["high-level"],
            ["interpreted"],
            ["dynamically typed", "dynamic typing"],
            ["object-oriented"],
            ["readable", "easy to read", "easy to understand"],
            ["standard library", "libraries"],
            ["cross-platform"]
        ]

    elif "list, tuple and set" in question_lower:

        concept_groups = [
            ["list"],
            ["mutable"],
            ["ordered"],
            ["tuple"],
            ["immutable"],
            ["set"],
            ["unique"],
            ["unordered"]
        ]

    elif "object-oriented programming" in question_lower:

        concept_groups = [
            ["class"],
            ["object"],
            ["inheritance"],
            ["encapsulation"],
            ["polymorphism"],
            ["abstraction"]
        ]

    elif "exception handling" in question_lower:

        concept_groups = [
            ["try"],
            ["except"],
            ["finally"],
            ["raise"],
            ["exception", "error"]
        ]

    elif "decorators and generators" in question_lower:

        concept_groups = [
            ["decorator"],
            ["wrapper"],
            ["function"],
            ["generator"],
            ["yield"],
            ["lazy"]
        ]

    elif "memory management" in question_lower:

        concept_groups = [
            ["memory"],
            ["heap"],
            ["garbage collection"],
            ["reference"],
            ["object"]
        ]

    elif "multiprocessing and multithreading" in question_lower:

        concept_groups = [
            ["multiprocessing"],
            ["multithreading"],
            ["process"],
            ["thread"],
            ["cpu"],
            ["gil"],
            ["parallel"]
        ]

    # ========================================================
    # FASTAPI
    # ========================================================

    elif question_lower == "what is fastapi?":

        concept_groups = [
            ["fastapi"],
            ["python"],
            ["web framework"],
            ["api", "apis", "rest api"],
            ["asynchronous", "async"],
            ["high performance", "performance"]
        ]

    elif (
        "why would you use fastapi" in question_lower
        or "why use fastapi" in question_lower
        or "traditional python web framework" in question_lower
        or (
            "what is fastapi" in question_lower
            and (
                "why would you use it" in question_lower
                or "why use it" in question_lower
                or "why do you use it" in question_lower
            )
        )
    ):

        concept_groups = [
            ["fastapi"],
            ["python"],
            ["web framework"],
            ["api", "apis", "rest api"],
            ["asynchronous", "async", "asynchronous programming"],
            ["high performance", "performance"],
            [
                "automatic documentation",
                "automatic api documentation",
                "api documentation",
                "swagger",
                "openapi"
            ],
            ["validation", "pydantic"]
        ]

    elif "dependency injection in fastapi" in question_lower:

        concept_groups = [
            ["dependency"],
            ["dependency injection"],
            ["depends"],
            ["reusable"],
        ]

    elif (
        "rest api" in question_lower
        and "fastapi" in question_lower
        and not is_scenario_question
    ):

        concept_groups = [
            ["endpoint", "endpoints"],
            ["get", "gets"],
            ["post", "posts"],
            ["put", "puts"],
            ["delete", "deletes"],
            ["http"],
            ["request", "requests"],
            ["response", "responses"]
        ]

    elif "secure a fastapi" in question_lower:

        concept_groups = [
            ["authentication"],
            ["authorization"],
            ["jwt"],
            ["https"],
            ["validation"],
            ["security", "secure", "securing"]
        ]

    elif "jwt" in question_lower:

        concept_groups = [
            ["jwt", "json web token"],
            ["token", "tokens"],
            ["authentication", "authenticate"],
            ["identity", "verify", "verification"],
            ["protected endpoint", "protected endpoints", "authorization"]
        ]

    elif "high traffic" in question_lower and "fastapi" in question_lower:

        concept_groups = [
            ["async", "asynchronous"],
            ["caching"],
            ["database"],
            ["connection pooling"],
            ["load balancing"],
            ["scaling"]
        ]

    # ========================================================
    # REACT
    # ========================================================

    elif question_lower == "what is react?":

        concept_groups = [
            ["javascript"],
            ["library"],
            ["user interface", "ui"],
            ["component"],
            ["frontend"]
        ]

    elif "react components" in question_lower:

        concept_groups = [
            ["component"],
            ["reusable"],
            ["ui"],
            ["props"],
            ["state"]
        ]

    elif "react hooks" in question_lower:

        concept_groups = [
            ["hooks"],
            ["usestate"],
            ["useeffect"],
            ["functional component"],
            ["state"],
            ["lifecycle"]
        ]

    elif "props and state" in question_lower:

        concept_groups = [
            ["props"],
            ["state"],
            ["immutable"],
            ["component"],
            ["data"]
        ]

    elif "virtual dom" in question_lower:

        concept_groups = [
            ["virtual dom"],
            ["dom"],
            ["diff"],
            ["reconciliation"],
            ["performance"]
        ]

    elif "optimize a react" in question_lower:

        concept_groups = [
            ["memoization"],
            ["usememo"],
            ["usecallback"],
            ["lazy loading"],
            ["code splitting"],
            ["virtual dom"]
        ]

    elif "useeffect and usememo" in question_lower:

        concept_groups = [
            ["useeffect"],
            ["side effect"],
            ["usememo"],
            ["memoization"],
            ["dependency"]
        ]

    # ========================================================
    # POSTGRESQL
    # ========================================================

    elif question_lower == "what is postgresql?":

        concept_groups = [
            ["database"],
            ["relational"],
            ["sql"],
            ["open source"],
            ["postgresql"]
        ]

    elif "primary key" in question_lower:

        concept_groups = [
            ["unique"],
            ["identify"],
            ["row", "record"],
            ["not null"]
        ]

    elif "foreign key" in question_lower:

        concept_groups = [
            ["relationship"],
            ["table"],
            ["reference"],
            ["primary key"]
        ]

    elif "sql and nosql" in question_lower:

        concept_groups = [
            ["sql"],
            ["relational"],
            ["structured"],
            ["nosql"],
            ["non relational"],
            ["schema"]
        ]

    elif "database indexing" in question_lower:

        concept_groups = [
            ["index"],
            ["search"],
            ["query"],
            ["performance"],
            ["database"]
        ]

    elif "slow postgresql query" in question_lower:

        concept_groups = [
            ["index"],
            ["query plan"],
            ["explain"],
            ["optimize"],
            ["database"]
        ]

    elif "normalization" in question_lower:

        concept_groups = [
            ["normalization"],
            ["redundancy"],
            ["duplicate"],
            ["table"],
            ["relationship"]
        ]

    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    elif question_lower == "what is machine learning?":

        concept_groups = [
            ["machine learning"],
            ["data"],
            ["model"],
            ["learn"],
            ["prediction"]
        ]

    elif "supervised and unsupervised" in question_lower:

        concept_groups = [
            ["supervised"],
            ["labeled"],
            ["unsupervised"],
            ["unlabeled"],
            ["classification"],
            ["clustering"]
        ]

    elif "overfitting" in question_lower:

        concept_groups = [
            ["overfitting"],
            ["training"],
            ["test"],
            ["generalization"],
            ["regularization"]
        ]

    elif "classification and regression" in question_lower:

        concept_groups = [
            ["classification"],
            ["regression"],
            ["categorical"],
            ["continuous"]
        ]

    elif "bias-variance" in question_lower:

        concept_groups = [
            ["bias"],
            ["variance"],
            ["overfitting"],
            ["underfitting"],
            ["generalization"]
        ]

    elif "imbalanced dataset" in question_lower:

        concept_groups = [
            ["imbalanced"],
            ["oversampling"],
            ["undersampling"],
            ["smote"],
            ["class weight"],
            ["precision", "recall"],
            ["f1"]
        ]

    elif "best features" in question_lower:

        concept_groups = [
            ["feature selection"],
            ["correlation"],
            ["importance"],
            ["selection"],
            ["model"]
        ]

    # ========================================================
    # DEEP LEARNING
    # ========================================================

    elif question_lower == "what is deep learning?":

        concept_groups = [
            ["neural network"],
            ["deep"],
            ["layers"],
            ["training"],
            ["data"]
        ]

    elif "artificial neural network" in question_lower:

        concept_groups = [
            ["neuron"],
            ["input"],
            ["hidden layer"],
            ["output"],
            ["weight"],
            ["bias"],
            ["activation"]
        ]

    elif "activation function" in question_lower:

        concept_groups = [
            ["activation"],
            ["nonlinear"],
            ["relu"],
            ["sigmoid"],
            ["tanh"]
        ]

    elif "backpropagation" in question_lower:

        concept_groups = [
            ["backpropagation"],
            ["gradient"],
            ["loss"],
            ["weight"],
            ["derivative"],
            ["update"]
        ]

    elif "vanishing and exploding gradients" in question_lower:

        concept_groups = [
            ["vanishing"],
            ["exploding"],
            ["gradient"],
            ["deep network"],
            ["relu"],
            ["normalization"]
        ]

    elif "cnn and rnn" in question_lower:

        concept_groups = [
            ["cnn"],
            ["rnn"],
            ["convolution"],
            ["sequence"],
            ["image"],
            ["temporal"]
        ]

    elif "transformers useful" in question_lower:

        concept_groups = [
            ["transformer"],
            ["attention"],
            ["parallel"],
            ["sequence"],
            ["nlp"]
        ]

    # ========================================================
    # NLP
    # ========================================================

    elif question_lower == "what is natural language processing?":

        concept_groups = [
            ["natural language"],
            ["text"],
            ["language"],
            ["computer"],
            ["processing"]
        ]

    elif "tokenization" in question_lower:

        concept_groups = [
            ["tokenization"],
            ["tokens"],
            ["words"],
            ["sentences"]
        ]

    elif "word embeddings" in question_lower:

        concept_groups = [
            ["embedding"],
            ["vector"],
            ["word"],
            ["semantic"],
            ["meaning"]
        ]

    elif "stemming and lemmatization" in question_lower:

        concept_groups = [
            ["stemming"],
            ["lemmatization"],
            ["root"],
            ["word"],
            ["dictionary"]
        ]

    elif "transformer models" in question_lower:

        concept_groups = [
            ["transformer"],
            ["attention"],
            ["encoder"],
            ["decoder"],
            ["sequence"]
        ]

    elif "attention work in nlp" in question_lower:

        concept_groups = [
            ["attention"],
            ["query"],
            ["key"],
            ["value"],
            ["context"]
        ]

    # ========================================================
    # TENSORFLOW
    # ========================================================

    elif question_lower == "what is tensorflow?":

        concept_groups = [
            ["tensorflow"],
            ["machine learning"],
            ["deep learning"],
            ["tensor"],
            ["model"]
        ]

    elif question_lower == "what is keras?":

        concept_groups = [
            ["keras"],
            ["deep learning"],
            ["neural network"],
            ["api"],
            ["tensorflow"]
        ]

    elif "neural network using tensorflow" in question_lower:

        concept_groups = [
            ["tensorflow"],
            ["model"],
            ["layer"],
            ["compile"],
            ["train"],
            ["fit"]
        ]

    elif "prevent overfitting in a tensorflow" in question_lower:

        concept_groups = [
            ["overfitting"],
            ["dropout"],
            ["regularization"],
            ["validation"],
            ["early stopping"]
        ]

    # ========================================================
    # PYTORCH
    # ========================================================

    elif question_lower == "what is pytorch?":

        concept_groups = [
            ["pytorch"],
            ["machine learning"],
            ["deep learning"],
            ["tensor"],
            ["model"]
        ]

    elif "what is a tensor" in question_lower:

        concept_groups = [
            ["tensor"],
            ["multi-dimensional"],
            ["array"],
            ["data"]
        ]

    elif "autograd" in question_lower:

        concept_groups = [
            ["autograd"],
            ["gradient"],
            ["automatic differentiation"],
            ["backpropagation"]
        ]

    # ========================================================
    # GIT
    # ========================================================

    elif question_lower == "what is git?":

        concept_groups = [
            ["git"],
            ["version control"],
            ["repository"],
            ["commit"],
            ["branch"]
        ]

    elif "git and github" in question_lower:

        concept_groups = [
            ["git"],
            ["github"],
            ["version control"],
            ["repository"]
        ]

    elif "git branch" in question_lower:

        concept_groups = [
            ["branch"],
            ["independent"],
            ["development"],
            ["merge"]
        ]

    elif "merge conflict" in question_lower:

        concept_groups = [
            ["merge conflict"],
            ["conflict"],
            ["resolve"],
            ["branch"],
            ["merge"]
        ]

    elif "git rebase" in question_lower:

        concept_groups = [
            ["rebase"],
            ["commit"],
            ["history"],
            ["branch"]
        ]

    # ========================================================
    # DOCKER
    # ========================================================

    elif question_lower == "what is docker?":

        concept_groups = [
            ["docker"],
            ["container"],
            ["image"],
            ["application"],
            ["isolated"]
        ]

    elif "docker container" in question_lower:

        concept_groups = [
            ["container"],
            ["isolated"],
            ["application"],
            ["image"]
        ]

    elif "docker image" in question_lower:

        concept_groups = [
            ["image"],
            ["template"],
            ["container"],
            ["layers"]
        ]

    elif "dockerize a fastapi" in question_lower:

        concept_groups = [
            ["dockerfile"],
            ["image"],
            ["container"],
            ["fastapi"],
            ["port"],
            ["deploy"]
        ]

    # ========================================================
    # AWS
    # ========================================================

    elif question_lower == "what is aws?":

        concept_groups = [
            ["aws"],
            ["cloud"],
            ["services"],
            ["infrastructure"],
            ["scalable"]
        ]

    elif "amazon ec2" in question_lower:

        concept_groups = [
            ["ec2"],
            ["virtual server"],
            ["compute"],
            ["instance"]
        ]

    elif "amazon s3" in question_lower:

        concept_groups = [
            ["s3"],
            ["object storage"],
            ["bucket"],
            ["storage"]
        ]

    # ========================================================
    # CUSTOM FASTAPI PROJECT QUESTION
    # ========================================================

    elif (
        "fastapi" in question_lower
        and "project" in question_lower
        and "endpoint" in question_lower
        and "validation" in question_lower
    ):

        concept_groups = [
            ["fastapi"],
            ["endpoint", "route"],
            ["request"],
            ["validation", "pydantic"],
            ["response"],
            ["api"]
        ]

    # ========================================================
    # CUSTOM JAVASCRIPT PROJECT QUESTION
    # ========================================================

    elif (
        "javascript" in question_lower
        and "project" in question_lower
    ):

        concept_groups = [
            ["javascript"],
            ["frontend", "client"],
            ["interaction"],
            ["api", "backend"],
            ["request", "response"],
            ["data"]
        ]

    # ========================================================
    # CUSTOM HTML PROJECT QUESTION
    # ========================================================

    elif (
        "html" in question_lower
        and "project" in question_lower
    ):

        concept_groups = [
            ["html"],
            ["structure"],
            ["element"],
            ["form"],
            ["frontend"]
        ]

    # ========================================================
    # CUSTOM CSS PROJECT QUESTION
    # ========================================================

    elif (
        "css" in question_lower
        and "project" in question_lower
    ):

        concept_groups = [
            ["css"],
            ["styling"],
            ["layout"],
            ["responsive"],
            ["design"]
        ]

    # ========================================================
    # CUSTOM MACHINE LEARNING PROJECT QUESTION
    # ========================================================

    elif (
        "machine learning" in question_lower
        and "project" in question_lower
    ):

        concept_groups = [
            ["machine learning"],
            ["data"],
            ["model"],
            ["training"],
            ["prediction", "classification", "regression"],
            ["evaluation", "accuracy", "precision", "recall"]
        ]

    # ========================================================
    # CUSTOM POSTGRESQL + FASTAPI QUESTION
    # ========================================================

    elif (
        "postgresql" in question_lower
        and "fastapi" in question_lower
    ):

        concept_groups = [
            ["postgresql"],
            ["database"],
            ["fastapi"],
            ["connection"],
            ["table"],
            ["query"],
            ["sqlalchemy", "orm"]
        ]

    # ========================================================
    # GENERIC SKILL QUESTION
    # ========================================================

    else:

        # Extract important technologies from the question.
        technology_terms = [
            "python",
            "fastapi",
            "react",
            "javascript",
            "html",
            "css",
            "sql",
            "postgresql",
            "machine learning",
            "deep learning",
            "nlp",
            "tensorflow",
            "pytorch",
            "git",
            "github",
            "docker",
            "aws",
            "computer vision"
        ]

        detected_technology = []

        for technology in technology_terms:

            if technology in question_lower:
                detected_technology.append(
                    technology
                )

        for technology in detected_technology:

            concept_groups.append(
                [technology]
            )

    # ========================================================
    # PROJECT QUESTION REQUIREMENTS
    # ========================================================

    if is_project_question:

        # Project questions must contain project-oriented
        # evidence, not simply technology names.

        concept_groups.extend([
            ["project", "application", "system"],
            ["used", "implemented", "developed", "built"],
            ["role", "responsibility", "worked"],
            ["problem", "purpose", "goal"],
            ["result", "outcome", "performance", "successfully", "achieved", "improved"]
        ])

    # ========================================================
    # SCENARIO QUESTION REQUIREMENTS
    # ========================================================

    if is_scenario_question and not (
        "high traffic" in question_lower
        and "fastapi" in question_lower
    ):

        concept_groups.extend([
            ["approach", "design", "implementation"],
            ["handle", "manage", "solve", "implement"],
            ["error", "validation", "security", "performance"]
        ])

    # ========================================================
    # BEHAVIORAL QUESTION REQUIREMENTS
    # ========================================================

    if is_behavioral_question:

        # Behavioral answers are evaluated using the
        # situation -> action -> result structure rather
        # than strict technical concepts.
        concept_groups = [
            ["situation", "scenario", "context", "faced"],
            ["problem", "issue", "challenge", "difficulty"],
            ["analyze", "analyzed", "identify", "identified", "understand", "checked"],
            ["action", "actions", "approach", "steps", "first", "testing", "improving"],
            ["solve", "solved", "solution", "fix", "fixed", "resolve", "resolved"],
            ["result", "results", "outcome", "success", "successfully"],
            ["learn", "learned", "experience", "improved", "improvement"]
        ]

    # ========================================================
    # HR QUESTION REQUIREMENTS
    # ========================================================

    if is_hr_question:

        # HR questions should not be evaluated like technical
        # questions.

        concept_groups = []

    # ========================================================
    # MATCH CONCEPT GROUPS
    # ========================================================

    matched_groups = []
    missing_groups = []

    for group in concept_groups:

        found = False

        for phrase in group:

            phrase_lower = phrase.lower().strip()

            if not phrase_lower:
                continue

            pattern = (
                r"\b"
                + re.escape(phrase_lower)
                + r"\b"
            )

            if re.search(
                pattern,
                answer_clean
            ):
                found = True
                break

        if found:
            matched_groups.append(
                group[0]
            )
        else:
            missing_groups.append(
                group[0]
            )

    total_groups = len(concept_groups)

    if total_groups > 0:

        concept_ratio = (
            len(matched_groups)
            /
            total_groups
        )

    else:

        concept_ratio = 0.0

    # ========================================================
    # DIRECT QUESTION INTENT CHECK
    # ========================================================

    question_skill_terms = [
        "python",
        "fastapi",
        "react",
        "javascript",
        "html",
        "css",
        "sql",
        "postgresql",
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "pytorch",
        "git",
        "github",
        "docker",
        "aws",
        "computer vision"
    ]

    question_skills = [
        skill
        for skill in question_skill_terms
        if skill in question_lower
    ]

    answer_skill_matches = [
        skill
        for skill in question_skills
        if skill in answer_clean
    ]

    # ========================================================
    # STRICT UNRELATED ANSWER DETECTION
    # ========================================================

    # If we have expected concepts and none are present,
    # the answer is not relevant.

    if (
        total_groups >= 2
        and len(matched_groups) == 0
    ):

        return {
            "score": 5,
            "overall_score": 5,

            "technical_score": 0,
            "project_score": 0,
            "communication_score": 0,
            "time_score": 0,
            "relevance_score": 0,

            "is_relevant": False,

            "feedback": (
                "Your answer does not address the "
                "question asked. The response appears "
                "to discuss a different topic."
            ),

            "strengths": [],

            "improvements": [
                "Read the question carefully.",
                "Answer the specific concept being asked.",
                "Avoid discussing unrelated technologies.",
                "Include the important concepts required by the question."
            ],

            "matched_topics": [],
            "project_topics": [],

            "word_count": word_count,
            "time_taken": safe_time_taken,
            "time_limit": safe_time_limit
        }

    # ========================================================
    # RELEVANCE SCORE
    # ========================================================

    if total_groups == 0:

        if is_hr_question:

            # ====================================================
            # HR RELEVANCE
            # ====================================================

            hr_relevance_terms = [
                "experience",
                "skills",
                "strength",
                "strengths",
                "weakness",
                "weaknesses",
                "project",
                "projects",
                "achievement",
                "achievements",
                "career",
                "goal",
                "goals",
                "team",
                "leadership",
                "communication",
                "problem solving",
                "problem-solving",
                "learning",
                "adaptable",
                "adaptability",
                "motivated",
                "motivation",
                "passionate",
                "interest",
                "interested",
                "contribute",
                "contribution",
                "company",
                "role",
                "position",
                "opportunity",
                "background",
                "education",
                "student",
                "developer"
            ]

            matched_hr_terms = [
                term
                for term in hr_relevance_terms
                if term in answer_lower
            ]

            hr_match_count = len(matched_hr_terms)

            if hr_match_count >= 5 and word_count >= 30:
                relevance_score = 95

            elif hr_match_count >= 3 and word_count >= 20:
                relevance_score = 85

            elif hr_match_count >= 2 and word_count >= 10:
                relevance_score = 70

            elif hr_match_count >= 1 and word_count >= 5:
                relevance_score = 50

            else:
                relevance_score = 20

        else:

            # General questions without concept groups.
            if word_count >= 30:
                relevance_score = 85

            elif word_count >= 15:
                relevance_score = 70

            elif word_count >= 5:
                relevance_score = 50

            else:
                relevance_score = 25

    else:

        matched_count = len(matched_groups)

    # Relevance measures how completely the answer
    # addresses the concepts required by the question.

        if concept_ratio >= 0.85 and matched_count >= 5:
            relevance_score = 95

        elif concept_ratio >= 0.70 and matched_count >= 4:
            relevance_score = 85

        elif concept_ratio >= 0.55 and matched_count >= 3:
            relevance_score = 72

        elif concept_ratio >= 0.40 and matched_count >= 2:
            relevance_score = 55

        elif concept_ratio >= 0.20 and matched_count >= 1:
            relevance_score = 30

        else:
            relevance_score = 10

    # A very short answer cannot receive excellent
    # relevance merely by mentioning the technology.

        if word_count < 20:
            relevance_score = min(
                relevance_score,
                65
            )

        if word_count < 10:
            relevance_score = min(
                relevance_score,
                45
            )
    # ========================================================
    # TECHNICAL SCORE
    # ========================================================
    if is_hr_question:

    # HR questions should not be penalized
    # for missing technical concepts.
        technical_score = 70

    elif is_behavioral_question:

        # Behavioral questions should not be judged
        # using strict technical concept matching.
        technical_score = 70

    elif total_groups == 0:

        technical_score = 50

    else:

        matched_count = len(matched_groups)

        # Strict technical scoring.
        # A technology name alone must not produce
        # a high technical score.

        if concept_ratio >= 0.85 and matched_count >= 5:
            technical_score = 95

        elif concept_ratio >= 0.70 and matched_count >= 4:
            technical_score = 85

        elif concept_ratio >= 0.55 and matched_count >= 3:
            technical_score = 75

        elif concept_ratio >= 0.40 and matched_count >= 2:
            technical_score = 60

        elif concept_ratio >= 0.20 and matched_count >= 1:
            technical_score = 40

        else:
            technical_score = 10

    # Short answers should not receive an excellent
    # technical score unless they contain enough
    # meaningful concepts.

    if word_count < 20 and not is_hr_question and not is_behavioral_question:
        technical_score = min(
            technical_score,
            60
        )

    if word_count < 10 and not is_hr_question and not is_behavioral_question:
        technical_score = min(
            technical_score,
            45
        )

    # ========================================================
    # PROJECT SCORE
    # ========================================================

    project_score = 0

    if is_project_question:

        project_evidence = [
            "project",
            "application",
            "system",
            "implemented",
            "developed",
            "built",
            "used",
            "deployed",
            "result",
            "outcome",
            "performance",
            "successfully",
            "achieved",
            "improved"
        ]

        project_matches = []

        for keyword in project_evidence:

            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(
                pattern,
                answer_clean
            ):
                project_matches.append(
                    keyword
                )

        project_matches = list(
            dict.fromkeys(
                project_matches
            )
        )

        if len(project_matches) >= 5:
            project_score = 95

        elif len(project_matches) >= 4:
            project_score = 85

        elif len(project_matches) >= 3:
            project_score = 70

        elif len(project_matches) >= 2:
            project_score = 50

        else:
            project_score = 20

    else:

        project_matches = []

    # ========================================================
    # COMMUNICATION SCORE
    # ========================================================

    if word_count >= 100:
        communication_score = 95

    elif word_count >= 70:
        communication_score = 90

    elif word_count >= 50:
        communication_score = 85

    elif word_count >= 30:
        communication_score = 78

    elif word_count >= 15:
        communication_score = 65

    elif word_count >= 5:
        communication_score = 50

    else:
        communication_score = 30

    # ========================================================
    # IMPORTANT:
    # UNRELATED ANSWERS CANNOT GET HIGH COMMUNICATION SCORE
    # ========================================================

    if relevance_score < 30:

        communication_score = min(
            communication_score,
            40
        )

    elif relevance_score < 50:

        communication_score = min(
            communication_score,
            60
        )

    # ========================================================
    # TIME SCORE
    # ========================================================

    if safe_time_taken <= safe_time_limit:

        ratio = (
            safe_time_taken
            /
            safe_time_limit
        )

        if ratio <= 0.70:
            time_score = 100

        elif ratio <= 0.85:
            time_score = 95

        else:
            time_score = 90

    else:

        overtime = (
            safe_time_taken
            -
            safe_time_limit
        )

        if overtime <= 10:
            time_score = 80

        elif overtime <= 20:
            time_score = 70

        elif overtime <= 30:
            time_score = 60

        else:
            time_score = 50

    # ========================================================
    # FINAL SCORE
    # ========================================================

    overall_score = round(
        (
            relevance_score * 0.45
            +
            technical_score * 0.35
            +
            project_score * 0.05
            +
            communication_score * 0.10
            +
            time_score * 0.05
        )
    )

    # ========================================================
    # STRICT SAFETY CAPS
    # ========================================================

    # --------------------------------------------------------
    # Very low relevance
    # --------------------------------------------------------

    if relevance_score < 20:

        overall_score = min(
            overall_score,
            10
        )

    elif relevance_score < 30:

        overall_score = min(
            overall_score,
            20
        )

    elif relevance_score < 40:

        overall_score = min(
            overall_score,
            35
        )

    elif relevance_score < 50:

        overall_score = min(
            overall_score,
            50
        )

    # --------------------------------------------------------
    # Low technical score
    # --------------------------------------------------------

    if technical_score < 20:

        overall_score = min(
            overall_score,
            25
        )

    # ========================================================
    # KEYWORD-ONLY PENALTY
    # ========================================================

    # If the answer mentions the technology but fails to
    # explain the required concepts, do not allow a high score.

    if (
        len(answer_skill_matches) > 0
        and concept_ratio < 0.40
        and total_groups >= 3
    ):

        overall_score = min(
            overall_score,
            35
        )

    # ========================================================
    # LONG BUT IRRELEVANT ANSWER PENALTY
    # ========================================================

    if (
        word_count >= 70
        and relevance_score < 40
    ):

        overall_score = min(
            overall_score,
            30
        )

    # ========================================================
    # PROJECT QUESTION STRICT CHECK
    # ========================================================

    if is_project_question:

        if project_score < 50:

            overall_score = min(
                overall_score,
                55
            )

        if relevance_score < 50:

            overall_score = min(
                overall_score,
                40
            )

    # ========================================================
    # STRENGTHS
    # ========================================================

    strengths = []

    if relevance_score >= 80:

        strengths.append(
            "Your answer directly addresses the question."
        )

    elif relevance_score >= 65:

        strengths.append(
            "Your answer addresses most of the question."
        )

    if technical_score >= 80:

        strengths.append(
            "Good technical understanding."
        )

    elif technical_score >= 65:

        strengths.append(
            "You included several relevant technical concepts."
        )

    if communication_score >= 80:

        strengths.append(
            "Your answer is clear and well explained."
        )

    if (
        is_project_question
        and project_score >= 70
    ):

        strengths.append(
            "Good connection between the answer and project experience."
        )

    if time_score >= 90:

        strengths.append(
            "Good time management."
        )

    # ========================================================
    # IMPROVEMENTS
    # ========================================================

    improvements = []

    if relevance_score < 75:

        improvements.append(
            "Focus more directly on what the question is asking."
        )

    if (
        technical_score < 75
        and not is_hr_question
        and not is_behavioral_question
    ):
        improvements.append(
            "Include more technically correct concepts "
            "related to the question."
        )

    if (
        is_project_question
        and project_score < 70
    ):

        improvements.append(
            "Connect your explanation to a specific project "
            "and describe your actual contribution."
        )

    if communication_score < 75:

        improvements.append(
            "Explain your answer in a clearer and more "
            "structured way."
        )

    if time_score < 80:

        improvements.append(
            "Try to complete your answer within the given time."
        )

    # ========================================================
    # MISSING CONCEPTS
    # ========================================================

    if (
        len(missing_groups) > 0
        and relevance_score >= 40
    ):

        important_missing = missing_groups[:3]

        if important_missing:

            improvements.append(
                "Important concepts to cover: "
                +
                ", ".join(
                    important_missing
                )
                +
                "."
            )

    # ========================================================
    # FEEDBACK
    # ========================================================

    if relevance_score < 20:

        feedback = (
            "Your answer does not address the question. "
            "It appears to discuss a different topic. "
            "Focus on the specific concept asked."
        )

    elif relevance_score < 40:

        feedback = (
            "Your answer is only partially related to "
            "the question. Focus on the exact topic and "
            "include the required technical concepts."
        )

    elif relevance_score < 60:

        feedback = (
            "Your answer is related to the question, "
            "but several important concepts are missing. "
            "Try to answer each part of the question."
        )

    elif relevance_score < 80:

        feedback = (
            "Good attempt. Your answer addresses the "
            "main topic, but adding the missing technical "
            "details would make it stronger."
        )

    elif technical_score < 75 and not is_behavioral_question:

        feedback = (
            "Your answer is relevant, but the technical "
            "explanation could be more accurate and complete."
        )

    elif is_project_question and project_score < 70:

        feedback = (
            "Your answer is technically relevant, but "
            "you should connect it more clearly to your "
            "actual project experience."
        )

    else:

        feedback = (
            "Excellent answer. Your response directly "
            "addresses the question and demonstrates "
            "strong understanding."
        )

    # ========================================================
    # FALLBACK IMPROVEMENTS
    # ========================================================

    if not improvements and not is_hr_question and not is_behavioral_question:
        improvements.append(
            "Continue providing specific, technically accurate explanations."
        )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "score": overall_score,
        "overall_score": overall_score,

        "technical_score":
            int(technical_score),

        "project_score":
            int(project_score),

        "communication_score":
            int(communication_score),

        "time_score":
            int(time_score),

        "relevance_score":
            int(relevance_score),

        "is_relevant": bool(
            relevance_score >= (40 if is_hr_question else 20)
        ),

        "feedback":
            feedback,

        "strengths":
            strengths,

        "improvements":
            improvements,

        "matched_topics":
            matched_groups,

        "project_topics":
            project_matches,

        "word_count":
            word_count,

        "time_taken":
            safe_time_taken,

        "time_limit":
            safe_time_limit
    }
