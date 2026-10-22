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

    elif question_lower == "what is fastapi?":

        expected = [
            "python",
            "web framework",
            "api",
            "rest",
            "asynchronous",
            "high performance"
        ]

    elif (
        "traditional python web framework"
        in question_lower
    ):

        expected = [
            "fastapi",
            "performance",
            "async",
            "type hints",
            "automatic documentation",
            "api"
        ]

    elif (
        "dependency injection in fastapi"
        in question_lower
    ):

        expected = [
            "dependency",
            "inject",
            "depends",
            "reusable",
            "dependency injection"
        ]

    elif "rest api" in question_lower:

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


def evaluate_interview_answer(
    question: str,
    answer: str,
    job_description: str,
    time_taken: int,
    time_limit: int = 90
) -> dict:
    """
    Intelligent interview answer evaluator.

    Evaluation is based on:
        1. Question type
        2. Relevance to the question
        3. Technical/content coverage
        4. Project relevance
        5. Communication quality
        6. Time management

    Important:
        - HR questions are NOT evaluated using technical keywords.
        - Project questions use project-specific criteria.
        - Resume skill questions use skill-specific criteria.
        - Scenario questions evaluate approach and reasoning.
        - Technical questions evaluate expected concepts.
        - A missing keyword alone does not automatically mean a 5%.
    """

    question = (question or "").strip()
    answer = (answer or "").strip()
    job_description = (job_description or "").strip()

    time_taken = max(
        0,
        int(time_taken or 0)
    )

    time_limit = max(
        1,
        int(time_limit or 90)
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

            "feedback": (
                "No answer was provided."
            ),

            "strengths": [],

            "improvements": [
                "Provide an answer to the question.",
                "Explain the main concept clearly.",
                "Use a relevant example where possible."
            ],

            "matched_topics": [],
            "project_topics": [],

            "word_count": 0,
            "time_taken": time_taken,
            "time_limit": time_limit
        }

    # ========================================================
    # TEXT NORMALIZATION
    # ========================================================

    question_lower = question.lower()
    answer_lower = answer.lower()

    answer_clean = re.sub(
        r"[^a-z0-9\s+#./_-]",
        " ",
        answer_lower
    )

    answer_clean = re.sub(
        r"\s+",
        " ",
        answer_clean
    ).strip()

    question_clean = re.sub(
        r"[^a-z0-9\s+#./_-]",
        " ",
        question_lower
    )

    question_clean = re.sub(
        r"\s+",
        " ",
        question_clean
    ).strip()

    word_count = len(
        answer.split()
    )

    # ========================================================
    # HELPER FUNCTIONS
    # ========================================================

    def contains_any(text, keywords):
        for keyword in keywords:

            keyword = str(
                keyword
            ).lower().strip()

            if not keyword:
                continue

            if keyword in text:
                return True

        return False

    def count_matches(text, keywords):

        matched = []

        for keyword in keywords:

            keyword = str(
                keyword
            ).lower().strip()

            if not keyword:
                continue

            if keyword in text:
                matched.append(
                    keyword
                )

        return list(
            dict.fromkeys(
                matched
            )
        )

    def percentage_from_ratio(ratio):

        ratio = max(
            0.0,
            min(
                1.0,
                ratio
            )
        )

        return round(
            ratio * 100
        )

    # ========================================================
    # DETECT QUESTION TYPE
    # ========================================================

    if contains_any(
        question_lower,
        [
            "tell me about yourself",
            "why are you interested",
            "why should we hire",
            "what are your strengths",
            "what are your weaknesses",
            "strengths and weaknesses",
            "where do you see yourself",
            "career goals",
            "why do you want",
            "why this role",
            "why this company"
        ]
    ):

        question_type = "HR"

    elif contains_any(
        question_lower,
        [
            "suppose",
            "imagine",
            "scenario",
            "how would you design",
            "how would you build",
            "how would you handle",
            "how would you implement",
            "if you were asked",
            "you are asked to"
        ]
    ):

        question_type = "Scenario"

    elif (
        "project" in question_lower
        and contains_any(
            question_lower,
            [
                "explain",
                "describe",
                "tell me",
                "mentioned in your resume",
                "from your resume"
            ]
        )
    ):

        question_type = "Project"

    elif contains_any(
        question_lower,
        [
            "you have listed",
            "listed on your resume",
            "mentioned in your resume",
            "how did you use",
            "describe how you used"
        ]
    ):

        question_type = "Resume Skill"

    elif contains_any(
        question_lower,
        [
            "required for this role",
            "role requires",
            "required for the role",
            "missing skill"
        ]
    ):

        question_type = "Job Requirement"

    else:

        question_type = "Technical"

    # ========================================================
    # TIME MANAGEMENT
    # ========================================================

    if time_taken <= 0:

        time_score = 100

    elif time_taken <= time_limit * 0.70:

        time_score = 100

    elif time_taken <= time_limit * 0.85:

        time_score = 95

    elif time_taken <= time_limit:

        time_score = 90

    elif time_taken <= time_limit * 1.15:

        time_score = 75

    else:

        time_score = 60

    # ========================================================
    # COMMUNICATION SCORE
    # ========================================================

    # Word count should NOT dominate the evaluation.
    # It only measures whether the answer has enough detail.

    if word_count >= 100:

        communication_score = 95

    elif word_count >= 70:

        communication_score = 90

    elif word_count >= 50:

        communication_score = 85

    elif word_count >= 35:

        communication_score = 78

    elif word_count >= 20:

        communication_score = 70

    elif word_count >= 10:

        communication_score = 55

    elif word_count >= 5:

        communication_score = 40

    else:

        communication_score = 25

    # ========================================================
    # SENTENCE / EXPLANATION QUALITY
    # ========================================================

    sentence_count = len(
        [
            sentence
            for sentence in re.split(
                r"[.!?]+",
                answer
            )
            if sentence.strip()
        ]
    )

    if sentence_count >= 4:

        communication_score = min(
            100,
            communication_score + 3
        )

    elif sentence_count >= 2:

        communication_score = min(
            100,
            communication_score + 1
        )

    # ========================================================
    # MATCHED TOPICS
    # ========================================================

    matched_topics = []

    try:

        question_topics = detect_question_topics(
            question
        )

        for topic in question_topics:

            keywords = QUESTION_TOPICS.get(
                topic,
                []
            )

            for keyword in keywords:

                keyword_lower = (
                    str(keyword)
                    .lower()
                    .strip()
                )

                if not keyword_lower:
                    continue

                if keyword_lower in answer_clean:

                    if keyword_lower != topic.lower():

                        matched_topics.append(
                            keyword
                        )

    except Exception:

        question_topics = []

    matched_topics = list(
        dict.fromkeys(
            matched_topics
        )
    )

    # ========================================================
    # QUESTION-SPECIFIC EVALUATION
    # ========================================================

    relevance_score = 0
    technical_score = 0
    project_score = 0

    expected_items = []
    matched_items = []

    # ========================================================
    # 1. HR QUESTIONS
    # ========================================================

    if question_type == "HR":

        hr_concepts = []

        if contains_any(
            question_lower,
            [
                "tell me about yourself",
                "background"
            ]
        ):

            hr_concepts = [
                "background",
                "education",
                "experience",
                "skills",
                "project",
                "career",
                "goal"
            ]

        elif contains_any(
            question_lower,
            [
                "why are you interested",
                "why this role",
                "why do you want"
            ]
        ):

            hr_concepts = [
                "interested",
                "role",
                "career",
                "experience",
                "skills",
                "project",
                "learning",
                "growth",
                "company",
                "contribute"
            ]

        elif contains_any(
            question_lower,
            [
                "why should we hire"
            ]
        ):

            hr_concepts = [
                "skills",
                "experience",
                "project",
                "strength",
                "contribute",
                "team",
                "learning"
            ]

        elif contains_any(
            question_lower,
            [
                "strengths and weaknesses",
                "strengths",
                "weaknesses"
            ]
        ):

            hr_concepts = [
                "strength",
                "weakness",
                "improve",
                "learning",
                "experience",
                "example"
            ]

        else:

            hr_concepts = [
                "experience",
                "skills",
                "project",
                "goal",
                "learning"
            ]

        expected_items = hr_concepts

        matched_items = count_matches(
            answer_clean,
            hr_concepts
        )

        # HR answers can be correct without
        # using exact expected words.
        #
        # Therefore project/skill terminology
        # receives additional relevance credit.

        practical_hr_terms = [
            "worked",
            "developed",
            "built",
            "created",
            "implemented",
            "used",
            "learned",
            "experience",
            "interested",
            "contribute",
            "team",
            "improve",
            "career",
            "role"
        ]

        practical_matches = count_matches(
            answer_clean,
            practical_hr_terms
        )

        concept_ratio = (
            len(matched_items)
            /
            max(
                1,
                len(expected_items)
            )
        )

        practical_ratio = min(
            1.0,
            len(practical_matches) / 5
        )

        relevance_score = round(
            (
                concept_ratio * 70
                +
                practical_ratio * 30
            )
        )

        # HR questions should not have
        # a technical score of zero simply
        # because they are HR questions.

        technical_score = min(
            100,
            50 + (
                len(matched_items) * 7
            )
        )

        # Project/experience references
        # are useful for HR answers.

        project_terms = [
            "project",
            "resume",
            "python",
            "fastapi",
            "react",
            "javascript",
            "sql",
            "postgresql",
            "machine learning",
            "api",
            "backend",
            "frontend"
        ]

        project_matches = count_matches(
            answer_clean,
            project_terms
        )

        project_score = min(
            100,
            50 + (
                len(project_matches) * 7
            )
        )

        # ----------------------------------------------------
        # HR FALLBACK
        # ----------------------------------------------------

        if word_count >= 20 and (
            len(practical_matches) >= 2
            or len(matched_items) >= 2
        ):

            relevance_score = max(
                relevance_score,
                70
            )

        if word_count >= 35 and (
            len(practical_matches) >= 3
        ):

            relevance_score = max(
                relevance_score,
                80
            )

    # ========================================================
    # 2. PROJECT QUESTIONS
    # ========================================================

    elif question_type == "Project":

        project_concepts = [
            "problem",
            "goal",
            "purpose",
            "role",
            "responsibility",
            "technology",
            "technologies",
            "python",
            "implementation",
            "developed",
            "built",
            "used",
            "result",
            "outcome",
            "challenge"
        ]

        expected_items = project_concepts

        matched_items = count_matches(
            answer_clean,
            project_concepts
        )

        # ----------------------------------------------------
        # Project technology detection
        # ----------------------------------------------------

        project_technology_terms = [
            "python",
            "yolov5",
            "opencv",
            "pytorch",
            "fastapi",
            "react",
            "javascript",
            "html",
            "css",
            "postgresql",
            "sql",
            "machine learning",
            "tensorflow",
            "scikit-learn",
            "google translate api",
            "gtts",
            "tkinter"
        ]

        technology_matches = count_matches(
            answer_clean,
            project_technology_terms
        )

        project_topics = technology_matches.copy()

        # ----------------------------------------------------
        # Project structure detection
        # ----------------------------------------------------

        problem_terms = [
            "problem",
            "goal",
            "purpose",
            "solve",
            "solved",
            "designed to"
        ]

        role_terms = [
            "my role",
            "i developed",
            "i implemented",
            "i worked",
            "i built",
            "i created",
            "i designed",
            "i integrated"
        ]

        technology_terms = [
            "python",
            "api",
            "framework",
            "library",
            "database",
            "model",
            "machine learning",
            "frontend",
            "backend"
        ]

        outcome_terms = [
            "result",
            "outcome",
            "successfully",
            "worked",
            "achieved",
            "improved",
            "application",
            "system"
        ]

        problem_found = contains_any(
            answer_clean,
            problem_terms
        )

        role_found = contains_any(
            answer_clean,
            role_terms
        )

        technology_found = (
            len(
                technology_matches
            ) >= 1
        )

        outcome_found = contains_any(
            answer_clean,
            outcome_terms
        )

        project_components = 0

        if problem_found:
            project_components += 1

        if role_found:
            project_components += 1

        if technology_found:
            project_components += 1

        if outcome_found:
            project_components += 1

        project_structure_score = (
            project_components
            /
            4
        ) * 100

        concept_ratio = (
            len(matched_items)
            /
            max(
                1,
                len(expected_items)
            )
        )

        relevance_score = round(
            min(
                100,
                (
                    concept_ratio * 50
                    +
                    project_structure_score * 50
                )
            )
        )

        technical_score = round(
            min(
                100,
                45
                +
                (
                    len(technology_matches)
                    * 10
                )
                +
                (
                    project_components
                    * 5
                )
            )
        )

        project_score = round(
            min(
                100,
                project_structure_score
                +
                min(
                    20,
                    len(
                        technology_matches
                    ) * 4
                )
            )
        )

        # ----------------------------------------------------
        # Project answer quality floor
        # ----------------------------------------------------

        if (
            word_count >= 35
            and technology_found
            and (
                role_found
                or problem_found
            )
        ):

            relevance_score = max(
                relevance_score,
                70
            )

        if (
            word_count >= 50
            and technology_found
            and role_found
            and outcome_found
        ):

            relevance_score = max(
                relevance_score,
                82
            )

    # ========================================================
    # 3. RESUME SKILL QUESTIONS
    # ========================================================

    elif question_type == "Resume Skill":

        skill = None

        known_skills = [
            "python",
            "fastapi",
            "react",
            "postgresql",
            "sql",
            "javascript",
            "html",
            "css",
            "machine learning",
            "deep learning",
            "nlp",
            "computer vision",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "git",
            "github",
            "c"
        ]

        for candidate in known_skills:

            if candidate in question_lower:

                skill = candidate
                break

        # ----------------------------------------------------
        # Skill-specific concepts
        # ----------------------------------------------------

        skill_concepts = {

            "python": [
                "python",
                "function",
                "library",
                "code",
                "backend",
                "data",
                "project",
                "implementation"
            ],

            "fastapi": [
                "fastapi",
                "api",
                "endpoint",
                "request",
                "response",
                "validation",
                "backend",
                "pydantic"
            ],

            "react": [
                "react",
                "component",
                "state",
                "props",
                "hook",
                "frontend",
                "ui",
                "api"
            ],

            "postgresql": [
                "postgresql",
                "database",
                "sql",
                "table",
                "query",
                "record",
                "backend"
            ],

            "sql": [
                "sql",
                "query",
                "select",
                "insert",
                "update",
                "delete",
                "database",
                "table"
            ],

            "javascript": [
                "javascript",
                "frontend",
                "api",
                "fetch",
                "json",
                "event",
                "dom",
                "form",
                "dynamic"
            ],

            "html": [
                "html",
                "structure",
                "frontend",
                "page",
                "form",
                "input",
                "label",
                "element",
                "semantic"
            ],

            "css": [
                "css",
                "style",
                "layout",
                "design",
                "responsive",
                "flexbox",
                "grid",
                "frontend"
            ],

            "machine learning": [
                "machine learning",
                "data",
                "model",
                "training",
                "prediction",
                "algorithm",
                "features",
                "evaluation"
            ],

            "deep learning": [
                "deep learning",
                "neural network",
                "model",
                "layers",
                "training",
                "prediction",
                "architecture"
            ],

            "nlp": [
                "nlp",
                "text",
                "language",
                "token",
                "preprocessing",
                "embedding",
                "model"
            ],

            "computer vision": [
                "computer vision",
                "image",
                "object",
                "detection",
                "opencv",
                "model",
                "processing"
            ],

            "tensorflow": [
                "tensorflow",
                "model",
                "training",
                "neural network",
                "keras",
                "layer",
                "prediction"
            ],

            "pytorch": [
                "pytorch",
                "tensor",
                "model",
                "training",
                "neural network",
                "backpropagation"
            ],

            "scikit-learn": [
                "scikit-learn",
                "model",
                "training",
                "preprocessing",
                "features",
                "prediction",
                "evaluation"
            ],

            "git": [
                "git",
                "repository",
                "commit",
                "branch",
                "version control",
                "merge"
            ],

            "github": [
                "github",
                "repository",
                "commit",
                "branch",
                "version control",
                "collaboration"
            ],

            "c": [
                "c",
                "program",
                "memory",
                "pointer",
                "function",
                "array",
                "programming"
            ]
        }

        if skill in skill_concepts:

            expected_items = (
                skill_concepts[skill]
            )

        else:

            expected_items = [
                "project",
                "used",
                "implemented",
                "developed",
                "experience"
            ]

        matched_items = count_matches(
            answer_clean,
            expected_items
        )

        # ----------------------------------------------------
        # Main skill itself should NOT be enough.
        # ----------------------------------------------------

        supporting_matches = [
            item
            for item in matched_items
            if item != skill
        ]

        concept_ratio = (
            len(supporting_matches)
            /
            max(
                1,
                len(expected_items) - 1
            )
        )

        relevance_score = percentage_from_ratio(
            min(
                1.0,
                concept_ratio
                +
                (
                    0.10
                    if word_count >= 20
                    else 0
                )
            )
        )

        technical_score = percentage_from_ratio(
            min(
                1.0,
                (
                    len(
                        supporting_matches
                    )
                    /
                    max(
                        1,
                        len(
                            expected_items
                        ) - 1
                    )
                )
                +
                0.15
            )
        )

        # Resume skill questions are practical
        # rather than pure definitions.

        practical_terms = [
            "project",
            "used",
            "implemented",
            "developed",
            "built",
            "created",
            "integrated",
            "application",
            "backend",
            "frontend"
        ]

        practical_matches = count_matches(
            answer_clean,
            practical_terms
        )

        project_score = min(
            100,
            50
            +
            (
                len(
                    practical_matches
                ) * 6
            )
        )

        # ----------------------------------------------------
        # Important quality floors
        # ----------------------------------------------------

        if (
            word_count >= 25
            and len(supporting_matches) >= 2
        ):

            relevance_score = max(
                relevance_score,
                65
            )

        if (
            word_count >= 40
            and len(supporting_matches) >= 3
        ):

            relevance_score = max(
                relevance_score,
                78
            )

    # ========================================================
    # 4. JOB REQUIREMENT QUESTIONS
    # ========================================================

    elif question_type == "Job Requirement":

        required_skill = None

        for candidate in [
            "python",
            "fastapi",
            "postgresql",
            "sql",
            "javascript",
            "react",
            "docker",
            "aws",
            "machine learning",
            "deep learning",
            "nlp"
        ]:

            if candidate in question_lower:

                required_skill = candidate
                break

        requirement_concepts = {

            "postgresql": [
                "postgresql",
                "database",
                "relational",
                "sql",
                "table",
                "query",
                "fastapi"
            ],

            "fastapi": [
                "fastapi",
                "api",
                "endpoint",
                "request",
                "response",
                "validation",
                "error"
            ],

            "python": [
                "python",
                "application",
                "function",
                "module",
                "library",
                "backend",
                "code"
            ],

            "sql": [
                "sql",
                "select",
                "insert",
                "update",
                "filter",
                "query",
                "database"
            ],

            "javascript": [
                "javascript",
                "api",
                "fetch",
                "json",
                "frontend",
                "event",
                "browser"
            ],

            "react": [
                "react",
                "component",
                "state",
                "props",
                "frontend",
                "ui",
                "reusable"
            ],

            "docker": [
                "docker",
                "container",
                "image",
                "dockerfile",
                "deployment",
                "application"
            ],

            "aws": [
                "aws",
                "cloud",
                "deployment",
                "ec2",
                "s3",
                "server"
            ]
        }

        expected_items = (
            requirement_concepts.get(
                required_skill,
                [
                    "knowledge",
                    "application",
                    "project",
                    "implementation"
                ]
            )
        )

        matched_items = count_matches(
            answer_clean,
            expected_items
        )

        concept_ratio = (
            len(matched_items)
            /
            max(
                1,
                len(expected_items)
            )
        )

        relevance_score = percentage_from_ratio(
            concept_ratio
        )

        technical_score = percentage_from_ratio(
            min(
                1.0,
                concept_ratio
                +
                0.10
            )
        )

        practical_terms = [
            "project",
            "application",
            "used",
            "implemented",
            "developed",
            "built",
            "would",
            "use"
        ]

        practical_matches = count_matches(
            answer_clean,
            practical_terms
        )

        project_score = min(
            100,
            45
            +
            len(
                practical_matches
            ) * 7
        )

        if (
            word_count >= 30
            and len(matched_items) >= 2
        ):

            relevance_score = max(
                relevance_score,
                65
            )

        if (
            word_count >= 45
            and len(matched_items) >= 3
        ):

            relevance_score = max(
                relevance_score,
                78
            )

    # ========================================================
    # 5. SCENARIO QUESTIONS
    # ========================================================

    elif question_type == "Scenario":

        scenario_concepts = [
            "design",
            "architecture",
            "implementation",
            "validate",
            "validation",
            "error",
            "handle",
            "database",
            "api",
            "endpoint",
            "security",
            "testing",
            "scaling",
            "deployment",
            "monitoring"
        ]

        expected_items = scenario_concepts

        matched_items = count_matches(
            answer_clean,
            scenario_concepts
        )

        # ----------------------------------------------------
        # Detect reasoning language
        # ----------------------------------------------------

        reasoning_terms = [
            "first",
            "then",
            "next",
            "after",
            "finally",
            "because",
            "therefore",
            "if",
            "would",
            "should",
            "step",
            "approach"
        ]

        reasoning_matches = count_matches(
            answer_clean,
            reasoning_terms
        )

        technical_terms = [
            "api",
            "endpoint",
            "database",
            "postgresql",
            "sql",
            "fastapi",
            "python",
            "validation",
            "authentication",
            "authorization",
            "error handling",
            "testing",
            "deployment",
            "docker",
            "aws",
            "model"
        ]

        technical_matches = count_matches(
            answer_clean,
            technical_terms
        )

        concept_ratio = (
            len(matched_items)
            /
            max(
                1,
                len(expected_items)
            )
        )

        reasoning_ratio = min(
            1.0,
            len(reasoning_matches) / 4
        )

        technical_ratio = min(
            1.0,
            len(technical_matches) / 5
        )

        relevance_score = percentage_from_ratio(
            (
                concept_ratio * 45
                +
                reasoning_ratio * 25
                +
                technical_ratio * 30
            )
        )

        technical_score = percentage_from_ratio(
            (
                concept_ratio * 60
                +
                technical_ratio * 40
            )
        )

        project_score = min(
            100,
            50
            +
            len(
                technical_matches
            ) * 6
        )

        if (
            word_count >= 40
            and len(reasoning_matches) >= 2
            and len(technical_matches) >= 2
        ):

            relevance_score = max(
                relevance_score,
                72
            )

        if (
            word_count >= 60
            and len(reasoning_matches) >= 3
            and len(technical_matches) >= 3
        ):

            relevance_score = max(
                relevance_score,
                82
            )

    # ========================================================
    # 6. TECHNICAL QUESTIONS
    # ========================================================

    else:

        # First use the existing expected-concept
        # engine.

        try:

            expected_items = (
                get_expected_concepts(
                    question
                )
                or []
            )

        except Exception:

            expected_items = []

        # ----------------------------------------------------
        # Additional skill-specific concepts
        # ----------------------------------------------------

        technical_fallbacks = {

            "python": [
                "programming language",
                "interpreted",
                "object-oriented",
                "dynamic",
                "library",
                "function"
            ],

            "fastapi": [
                "api",
                "endpoint",
                "request",
                "response",
                "validation",
                "pydantic",
                "async"
            ],

            "react": [
                "component",
                "state",
                "props",
                "hooks",
                "frontend",
                "ui"
            ],

            "postgresql": [
                "database",
                "relational",
                "sql",
                "table",
                "query",
                "index"
            ],

            "machine learning": [
                "data",
                "algorithm",
                "training",
                "model",
                "prediction",
                "features"
            ],

            "deep learning": [
                "neural network",
                "layers",
                "training",
                "model",
                "activation",
                "gradient"
            ],

            "pytorch": [
                "tensor",
                "model",
                "training",
                "gradient",
                "autograd"
            ],

            "tensorflow": [
                "model",
                "training",
                "tensor",
                "neural network",
                "keras"
            ],

            "git": [
                "repository",
                "commit",
                "branch",
                "version control",
                "merge"
            ],

            "docker": [
                "container",
                "image",
                "dockerfile",
                "deployment",
                "dependencies"
            ],

            "aws": [
                "cloud",
                "deployment",
                "ec2",
                "s3",
                "server"
            ]
        }

        detected_skill = None

        for skill in technical_fallbacks:

            if skill in question_lower:

                detected_skill = skill
                break

        if not expected_items:

            if detected_skill:

                expected_items = (
                    technical_fallbacks[
                        detected_skill
                    ]
                )

            else:

                expected_items = [
                    "concept",
                    "explain",
                    "example",
                    "application"
                ]

        matched_items = count_matches(
            answer_clean,
            expected_items
        )

        concept_ratio = (
            len(matched_items)
            /
            max(
                1,
                len(expected_items)
            )
        )

        topic_ratio = min(
            1.0,
            len(matched_topics) / 4
        )

        relevance_score = percentage_from_ratio(
            min(
                1.0,
                (
                    concept_ratio * 75
                    +
                    topic_ratio * 25
                )
            )
        )

        technical_score = percentage_from_ratio(
            concept_ratio
        )

        project_terms = [
            "project",
            "application",
            "implemented",
            "developed",
            "built",
            "used",
            "example",
            "real world"
        ]

        project_matches = count_matches(
            answer_clean,
            project_terms
        )

        project_score = min(
            100,
            45
            +
            len(
                project_matches
            ) * 7
        )

        if (
            word_count >= 25
            and len(matched_items) >= 2
        ):

            relevance_score = max(
                relevance_score,
                65
            )

        if (
            word_count >= 45
            and len(matched_items) >= 3
        ):

            relevance_score = max(
                relevance_score,
                78
            )

    # ========================================================
    # JOB DESCRIPTION RELEVANCE
    # ========================================================

    job_skill_matches = []

    if job_description:

        job_lower = job_description.lower()

        common_job_skills = [
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
            "computer vision",
            "tensorflow",
            "pytorch",
            "scikit-learn",
            "git",
            "github",
            "docker",
            "aws"
        ]

        for skill in common_job_skills:

            if skill in job_lower:

                if skill in answer_lower:

                    job_skill_matches.append(
                        skill
                    )

    # Job relevance should be a small
    # supporting factor, not the main score.

    if job_skill_matches:

        relevance_score = min(
            100,
            relevance_score
            +
            min(
                10,
                len(
                    job_skill_matches
                ) * 3
            )
        )

    # ========================================================
    # UNRELATED ANSWER DETECTION
    # ========================================================

    # We DO NOT immediately return 5 merely
    # because there are no exact keywords.
    #
    # First check whether the answer has
    # meaningful language related to the
    # question type.

    generic_relevant_terms = [
        "project",
        "experience",
        "used",
        "worked",
        "developed",
        "built",
        "implemented",
        "application",
        "system",
        "role",
        "skill",
        "technology",
        "approach",
        "problem",
        "solution",
        "result",
        "because",
        "example",
        "learned"
    ]

    generic_matches = count_matches(
        answer_clean,
        generic_relevant_terms
    )

    no_content_signal = (
        len(matched_items) == 0
        and len(matched_topics) == 0
        and len(generic_matches) == 0
    )

    if no_content_signal:

        relevance_score = min(
            relevance_score,
            15
        )

        technical_score = min(
            technical_score,
            10
        )

        project_score = min(
            project_score,
            10
        )

    # ========================================================
    # RELEVANCE LOWER BOUND
    # ========================================================

    if (
        word_count >= 20
        and (
            len(matched_items) >= 2
            or len(matched_topics) >= 1
            or len(generic_matches) >= 3
        )
        and not no_content_signal
    ):

        relevance_score = max(
            relevance_score,
            55
        )

    # ========================================================
    # STRENGTHS
    # ========================================================

    strengths = []

    if relevance_score >= 80:

        strengths.append(
            "Your answer directly addresses the question."
        )

    elif relevance_score >= 60:

        strengths.append(
            "Your answer is relevant to the question."
        )

    if technical_score >= 80:

        strengths.append(
            "You included strong technical concepts."
        )

    elif technical_score >= 60:

        strengths.append(
            "You included some relevant technical concepts."
        )

    if project_score >= 80:

        strengths.append(
            "You connected the answer with practical project experience."
        )

    elif project_score >= 60:

        strengths.append(
            "You included practical or project-related information."
        )

    if communication_score >= 85:

        strengths.append(
            "Your answer is clear and well explained."
        )

    elif communication_score >= 70:

        strengths.append(
            "Your answer provides a reasonable amount of detail."
        )

    if time_score >= 90:

        strengths.append(
            "Good time management."
        )

    # ========================================================
    # IMPROVEMENTS
    # ========================================================

    improvements = []

    if relevance_score < 60:

        improvements.append(
            "Focus more directly on what the question is asking."
        )

    elif relevance_score < 80:

        improvements.append(
            "Make the connection between your answer and the question more explicit."
        )

    if technical_score < 60:

        if question_type in [
            "Technical",
            "Resume Skill",
            "Job Requirement",
            "Scenario"
        ]:

            improvements.append(
                "Include more technically correct concepts related to the question."
            )

    if project_score < 60:

        if question_type in [
            "Project",
            "Resume Skill",
            "HR",
            "Scenario"
        ]:

            improvements.append(
                "Connect your explanation to a relevant project or practical example where appropriate."
            )

    if communication_score < 60:

        improvements.append(
            "Give a more complete answer with a clear beginning, explanation, and conclusion."
        )

    if (
        question_type == "Project"
        and not project_topics
    ):

        improvements.append(
            "Mention the specific technologies you used in the project."
        )

    if (
        question_type == "Project"
        and not outcome_found
        if "outcome_found" in locals()
        else False
    ):

        improvements.append(
            "Explain the result or outcome of the project."
        )

    if (
        question_type == "Scenario"
        and word_count < 40
    ):

        improvements.append(
            "Explain your solution step by step."
        )

    if (
        question_type == "HR"
        and word_count < 25
    ):

        improvements.append(
            "Add a specific example from your experience."
        )

    if time_score < 75:

        improvements.append(
            "Try to manage the available interview time more effectively."
        )

    # Remove duplicate improvements

    improvements = list(
        dict.fromkeys(
            improvements
        )
    )

    # ========================================================
    # FALLBACK STRENGTH
    # ========================================================

    if not strengths:

        if word_count >= 15:

            strengths.append(
                "You provided an attempt and communicated your response."
            )

        else:

            strengths.append(
                "You started addressing the question."
            )

    # ========================================================
    # FEEDBACK
    # ========================================================

    if no_content_signal:

        feedback = (
            "Your answer does not sufficiently address "
            "the question. Try to focus on the specific "
            "topic and include relevant concepts or an "
            "example from your experience."
        )

    elif relevance_score >= 85:

        feedback = (
            "Excellent answer. You addressed the question "
            "directly and included relevant details."
        )

    elif relevance_score >= 75:

        feedback = (
            "Good answer. You addressed the main requirement "
            "of the question, but adding a little more "
            "specific detail would make it stronger."
        )

    elif relevance_score >= 60:

        feedback = (
            "Your answer is relevant, but it could be more "
            "specific and technically detailed."
        )

    else:

        feedback = (
            "Your answer is partially related to the question. "
            "Focus on the specific concept being asked and "
            "support your explanation with a relevant example."
        )

    # ========================================================
    # FINAL OVERALL SCORE
    # ========================================================

    # Different question types require
    # different scoring weights.

    if question_type == "HR":

        overall_score = round(
            (
                relevance_score * 0.40
                +
                technical_score * 0.10
                +
                project_score * 0.15
                +
                communication_score * 0.25
                +
                time_score * 0.10
            )
        )

    elif question_type == "Project":

        overall_score = round(
            (
                relevance_score * 0.30
                +
                technical_score * 0.20
                +
                project_score * 0.30
                +
                communication_score * 0.15
                +
                time_score * 0.05
            )
        )

    elif question_type == "Scenario":

        overall_score = round(
            (
                relevance_score * 0.30
                +
                technical_score * 0.30
                +
                project_score * 0.15
                +
                communication_score * 0.15
                +
                time_score * 0.10
            )
        )

    else:

        overall_score = round(
            (
                relevance_score * 0.35
                +
                technical_score * 0.35
                +
                project_score * 0.10
                +
                communication_score * 0.15
                +
                time_score * 0.05
            )
        )

    # ========================================================
    # FINAL SAFETY LIMITS
    # ========================================================

    overall_score = max(
        0,
        min(
            100,
            overall_score
        )
    )

    relevance_score = max(
        0,
        min(
            100,
            round(relevance_score)
        )
    )

    technical_score = max(
        0,
        min(
            100,
            round(technical_score)
        )
    )

    project_score = max(
        0,
        min(
            100,
            round(project_score)
        )
    )

    communication_score = max(
        0,
        min(
            100,
            round(communication_score)
        )
    )

    time_score = max(
        0,
        min(
            100,
            round(time_score)
        )
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "score": overall_score,
        "overall_score": overall_score,

        "technical_score": technical_score,
        "project_score": project_score,
        "communication_score": communication_score,
        "time_score": time_score,
        "relevance_score": relevance_score,

        "is_relevant": (
            relevance_score >= 40
        ),

        "feedback": feedback,

        "strengths": strengths,

        "improvements": improvements,

        "matched_topics": list(
            dict.fromkeys(
                matched_items
                +
                matched_topics
            )
        ),

        "project_topics": list(
            dict.fromkeys(
                project_topics
                if "project_topics"
                in locals()
                else []
            )
        ),

        "word_count": word_count,

        "time_taken": time_taken,

        "time_limit": time_limit
    }