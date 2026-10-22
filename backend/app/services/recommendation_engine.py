RECOMMENDATIONS = {

    "Python": {
        "reason": "Python is widely used for backend development, data science and AI.",
        "actions": [
            "Practice Python OOP and data structures.",
            "Build a Python-based project.",
            "Use Python in an AI or backend application."
        ]
    },

    "FastAPI": {
        "reason": "FastAPI is useful for building high-performance Python APIs.",
        "actions": [
            "Learn FastAPI routing and dependency injection.",
            "Build REST APIs using FastAPI.",
            "Connect FastAPI with PostgreSQL."
        ]
    },

    "React": {
        "reason": "React is widely used for modern frontend applications.",
        "actions": [
            "Learn React components and hooks.",
            "Build a dashboard using React.",
            "Connect React with a FastAPI backend."
        ]
    },

    "PostgreSQL": {
        "reason": "PostgreSQL is a popular relational database.",
        "actions": [
            "Learn SQL queries and joins.",
            "Practice PostgreSQL database design.",
            "Connect PostgreSQL with FastAPI."
        ]
    },

    "Docker": {
        "reason": "Docker is important for application deployment and DevOps.",
        "actions": [
            "Learn Docker images and containers.",
            "Create a Dockerfile for your project.",
            "Dockerize your FastAPI application."
        ]
    },

    "AWS": {
        "reason": "AWS provides cloud infrastructure for deploying applications.",
        "actions": [
            "Learn AWS EC2 and S3 basics.",
            "Understand cloud deployment.",
            "Deploy a small application on AWS."
        ]
    },

    "Machine Learning": {
        "reason": "Machine Learning is important for building intelligent applications.",
        "actions": [
            "Learn supervised and unsupervised learning.",
            "Practice Scikit-learn.",
            "Build an end-to-end ML project."
        ]
    },

    "Deep Learning": {
        "reason": "Deep Learning is useful for advanced AI applications.",
        "actions": [
            "Learn neural networks and backpropagation.",
            "Practice CNNs and RNNs.",
            "Build a deep learning project."
        ]
    },

    "NLP": {
        "reason": "NLP is useful for understanding and processing human language.",
        "actions": [
            "Learn text preprocessing.",
            "Learn embeddings and transformers.",
            "Build an NLP-based project."
        ]
    },

    "TensorFlow": {
        "reason": "TensorFlow is a popular framework for deep learning.",
        "actions": [
            "Learn TensorFlow fundamentals.",
            "Build neural networks using Keras.",
            "Train and evaluate a deep learning model."
        ]
    },

    "PyTorch": {
        "reason": "PyTorch is widely used for deep learning and AI research.",
        "actions": [
            "Learn tensors and neural networks.",
            "Build a model using PyTorch.",
            "Practice training and evaluation."
        ]
    },

    "Git": {
        "reason": "Git is essential for version control and collaborative development.",
        "actions": [
            "Learn Git branches and commits.",
            "Use Git for your projects.",
            "Practice GitHub collaboration."
        ]
    },

    "GitHub": {
        "reason": "GitHub is widely used for hosting and collaborating on code.",
        "actions": [
            "Create a professional GitHub repository.",
            "Write a good README.",
            "Maintain your projects using GitHub."
        ]
    },

    "Computer Vision": {
        "reason": "Computer Vision enables applications to understand images and video.",
        "actions": [
            "Learn image preprocessing.",
            "Study CNN architectures.",
            "Build an image classification project."
        ]
    }
}


def generate_recommendations(
    missing_skills: list,
    interview_history: list | None = None
) -> list:

    recommendations = []

    # ------------------------------------------------------------
    # Normalize interview history
    # ------------------------------------------------------------

    interview_history = interview_history or []

    # Store interview scores by skill
    skill_scores = {}

    for interview in interview_history:

        # Support SQLAlchemy objects
        if hasattr(interview, "skill"):
            skill = interview.skill
            score = interview.score
        else:
            skill = interview.get("skill")
            score = interview.get("score", 0)

        if not skill:
            continue

        try:
            score = float(score or 0)
        except (TypeError, ValueError):
            score = 0

        # Some questions may contain multiple skills
        skills = [
            item.strip()
            for item in str(skill).split(",")
            if item.strip()
        ]

        for item in skills:

            key = item.lower()

            if key not in skill_scores:
                skill_scores[key] = {
                    "skill": item,
                    "scores": []
                }

            skill_scores[key]["scores"].append(score)

    # ------------------------------------------------------------
    # Calculate average interview score
    # ------------------------------------------------------------

    skill_averages = {}

    for key, data in skill_scores.items():

        scores = data["scores"]

        if scores:
            skill_averages[key] = {
                "skill": data["skill"],
                "average": round(
                    sum(scores) / len(scores),
                    2
                )
            }

    # ------------------------------------------------------------
    # 1. Missing job skills
    # ------------------------------------------------------------

    for skill in missing_skills:

        recommendation = RECOMMENDATIONS.get(skill)

        if recommendation:

            recommendations.append({
                "skill": skill,
                "priority": "HIGH",
                "category": "Missing Job Skill",
                "reason": (
                    f"{skill} is required for the target job "
                    "but is currently missing from your resume."
                ),
                "actions": recommendation["actions"]
            })

        else:

            recommendations.append({
                "skill": skill,
                "priority": "HIGH",
                "category": "Missing Job Skill",
                "reason": (
                    f"{skill} is required for the target job "
                    "but is currently missing from your resume."
                ),
                "actions": [
                    f"Learn the fundamentals of {skill}.",
                    f"Build a practical project using {skill}.",
                    (
                        f"Add {skill} to your resume "
                        "after gaining practical experience."
                    )
                ]
            })

    # ------------------------------------------------------------
    # 2. Weak interview skills
    # ------------------------------------------------------------

    missing_lower = {
        str(skill).lower()
        for skill in missing_skills
    }

    for key, data in skill_averages.items():

        skill = data["skill"]
        average = data["average"]

        # Do not duplicate missing job skills
        if key in missing_lower:
            continue

        # Only recommend skills with weak interview performance
        if average < 70:

            recommendation = RECOMMENDATIONS.get(
                skill
            )

            if recommendation:

                actions = recommendation["actions"]

                reason = (
                    f"Your average interview score for "
                    f"{skill} is {average}%. "
                    "Improving this skill can strengthen "
                    "your interview performance."
                )

            else:

                reason = (
                    f"Your average interview score for "
                    f"{skill} is {average}%. "
                    "You should strengthen your practical "
                    "understanding of this skill."
                )

                actions = [
                    f"Review the fundamentals of {skill}.",
                    f"Practice technical questions related to {skill}.",
                    f"Build a small project using {skill}."
                ]

            recommendations.append({
                "skill": skill,
                "priority": "MEDIUM",
                "category": "Interview Weakness",
                "reason": reason,
                "actions": actions
            })

            # Sort recommendations by priority
            priority_order = {
                "HIGH": 1,
                "MEDIUM": 2,
                "LOW": 3
            }

            recommendations.sort(
                key=lambda item: (
                    priority_order.get(
                        item.get("priority", "LOW"),
                        3
                    ),
                    item.get("skill", "").lower()
                )
            )


    return recommendations