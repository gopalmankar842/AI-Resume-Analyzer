
import re

from app.services.resume_analyzer import (
    extract_skills,
    get_flattened_skills,
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def has_term(text: str, term: str) -> bool:
    pattern = r"(?<!\w)" + re.escape(term.lower()) + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None

def check_ats(resume_text: str, job_description: str) -> dict:
    """
    Estimate ATS compatibility using keywords, sections, and text length.
    This is a heuristic, not an actual employer ATS score.
    """
    resume = normalize(resume_text)
    job = normalize(job_description)

    if not resume:
        raise ValueError("Resume text is empty.")
    if not job:
        raise ValueError("Job description is empty.")

    resume_skills = get_flattened_skills(extract_skills(resume))
    job_skills = list(dict.fromkeys(
        get_flattened_skills(extract_skills(job))
    ))

    matched_skills = [
        skill for skill in job_skills
        if has_term(resume, skill)
    ]
    missing_skills = [
        skill for skill in job_skills
        if skill not in matched_skills
    ]

    keyword_score = (
        round(100 * len(matched_skills) / len(job_skills))
        if job_skills else 0
    )

    sections = {
        "contact_information": ["email","e-mail","phone","mobile","contact","linkedin","github.com","@" ,"+91",
        ],
        "skills": [
            "skills", "technical skills", "key skills",
            "core competencies", "technical expertise",
        ],
        "education": [
            "education", "academic background", "academic qualifications",
            "educational qualifications", "education details", "academic details",
        ],
        "experience": [
            "experience", "work experience", "professional experience",
            "internship", "work history",
        ],
        "projects": [
            "projects", "academic projects", "personal projects",
            "project experience",
        ],
    }

    sections_found = {
        section: any(has_term(resume, term) for term in terms)
        for section, terms in sections.items()
    }

    section_score = round(
        100 * sum(sections_found.values()) / len(sections_found)
    ) if sections_found else 0

    word_count = len(resume.split())
    warnings = []

    if word_count < 100:
        warnings.append(
            "Very little text was extracted. Check whether the PDF "
            "contains selectable text or needs OCR."
        )
    elif word_count < 250:
        warnings.append(
            "The resume is short. Check whether relevant details are missing."
        )

    if not sections_found["contact_information"]:
        warnings.append("Contact information was not clearly detected.")
    if not sections_found["education"]:
        warnings.append("An education section was not clearly detected.")
    if not sections_found["skills"]:
        warnings.append("A skills section was not clearly detected.")

    readability_score = (
        30 if word_count < 100
        else 60 if word_count < 250
        else 100
    )

    overall_score = round(
        keyword_score * 0.60
        + section_score * 0.25
        + readability_score * 0.15
    )

    suggestions = []

    if missing_skills:
        suggestions.append(
            "If you genuinely have these skills, add relevant evidence "
            "to your resume: " + ", ".join(missing_skills)
        )

    if section_score < 100:
        suggestions.append(
            "Review the resume sections that were not detected."
        )

    if word_count < 250:
        suggestions.append(
            "Check whether your projects, experience, and achievements "
            "are described adequately."
        )

    if not suggestions:
        suggestions.append(
            "Review the job requirements and verify every claim "
            "before applying."
        )

    return {
        "ats_score": overall_score,
        "score_type": "Estimated ATS compatibility",
        "score_breakdown": {
            "keyword_match": keyword_score,
            "section_completeness": section_score,
            "readability": readability_score,
        },
        "word_count": word_count,
        "job_skills_found": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "sections_found": sections_found,
        "warnings": warnings,
        "suggestions": suggestions,
        "disclaimer": (
            "This is a heuristic estimate, not a score from an "
            "employer's ATS. Different systems use different rules."
        ),
    }


def check_resume_ats_score(resume_text: str) -> dict:
    """
    Estimate general resume readiness using transparent, rule-based checks.
    This is not an official ATS score or a job-specific compatibility score.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    original_text = resume_text
    print("\n===== EXTRACTED RESUME TEXT =====\n")
    print(original_text)
    text = re.sub(r"\s+", " ", original_text.lower()).strip()

    lines = [
        re.sub(r"\s+", " ", line).strip(" \t•▪●|-")
        for line in original_text.splitlines()
        if line.strip()
    ]

    word_count = len(text.split())
    warnings = []
    suggestions = []

    # Recognize actual section headings, including common alternatives.
    # These are aliases, not keywords searched anywhere in the resume.
    section_patterns = {
        "summary": [
            "professional summary", "career objective",
            "career summary", "professional profile",
            "objective", "summary", "profile",
        ],
        "skills": [
            "technical skills", "key skills",
            "core competencies", "technical expertise",
            "skills",
        ],
        "education": ["academic qualifications","academic background",
        "educational qualifications","education",
        ],
        "experience": [
            "professional experience","work experience","work experience recommendations",
            "internship experience","employment history","work history","internships",
            "internship","experience",
        ],
        "projects": [
            "key projects","academic projects","personal projects","technical projects","selected projects",
            "relevant projects","project experience","projects","project",
        ],
        "certifications": [
            "licenses and certifications", "certifications",
            "certificates",
            "certifications & achievements",
            "certifications and achievements",
        ],
        "achievements": [
            "competitive programming, open source & achievements","competitive programming, open source and achievements",
            "awards and honors","honors and awards","accomplishments","achievements",
        ],
    }

    
    def find_heading_matches(line):
        """Recognize one or more sections from a heading line."""
        cleaned = line.strip().lower()
        matches = []

        for section, patterns in section_patterns.items():
            for alias in patterns:
                match = re.match(
                    r"^\s*" + re.escape(alias)
                    + r"(?=$|[\s:|–—-])",
                    cleaned,
                    flags=re.IGNORECASE,
                )
                if match:
                    matches.append(
                        (len(alias), section, match.end())
                    )

        if not matches:
            return []

        # Use the longest matching heading alias to avoid confusing
        # "Key Projects" with a shorter heading such as "Projects".
        longest_length = max(length for length, _, _ in matches)

        best_matches = [
            item for item in matches
            if item[0] == longest_length
        ]

        # A combined heading can belong to multiple sections.
        # Keep every section matching the same longest alias.
        result = []
        seen_sections = set()

        for _, section, end_position in best_matches:
            if section not in seen_sections:
                remainder = cleaned[end_position:].lstrip(" \t:|–—-")
                result.append((section, remainder))
                seen_sections.add(section)

        return result

    headings = []

    for index, line in enumerate(lines):
        for section, remainder in find_heading_matches(line):
            headings.append((index, section, remainder))

    sections_found = {
        section: any(
            found_section == section
            for _, found_section, _ in headings
        )
        for section in section_patterns
    }


    def section_has_content(section_name):
        """Check for descriptive text belonging to a detected section."""
        positions = [
            (index, remainder)
            for index, section, remainder in headings
            if section == section_name
        ]

        for index, remainder in positions:
            if len(remainder.split()) >= 3:
                return True

            # Stop at the next recognized heading, so content from a
            # different section is not credited to this one.
            next_heading_index = next(
                (
                    heading_index
                    for heading_index, _, _ in headings
                    if heading_index > index
                ),
                len(lines),
            )

            for line in lines[index + 1:next_heading_index]:
                if len(line.split()) >= 3:
                    return True

        return False

    sections_with_content = {
        section: sections_found[section]
        and section_has_content(section)
        for section in section_patterns
    }

    # 1. Structure: section presence, not section quality.
    section_score = round(
        100 * sum(sections_found.values()) / len(section_patterns)
    )

    # 2. Contact details.
    email_found = bool(re.search(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        original_text,
        flags=re.IGNORECASE,
    ))

    phone_found = bool(re.search(
        r"(?<!\w)(?:\+\d{1,3}[\s.-]?)?"
        r"(?:\(?\d{3,5}\)?[\s.-]?)?\d{5,10}(?!\w)",
        original_text,
    ))

    contact_score = round(
        100 * (int(email_found) + int(phone_found)) / 2
    )

    if not email_found:
        warnings.append("A recognizable email address was not detected.")
        suggestions.append(
            "Check that your email address is present and readable."
        )

    if not phone_found:
        warnings.append("A recognizable phone number was not detected.")

    # 3. Skills: unique recognized skills, with a clearly labelled section.
    extracted_skills = get_flattened_skills(extract_skills(text))
    unique_skills = list(dict.fromkeys(
        str(skill).strip()
        for skill in extracted_skills
        if skill and str(skill).strip()
    ))

    if sections_found["skills"]:
        skills_score = min(100, round(len(unique_skills) / 8 * 100))
    else:
        skills_score = min(60, round(len(unique_skills) / 8 * 60))

    if not sections_found["skills"]:
        suggestions.append(
            "Use a clearly labelled Skills or Technical Skills section."
        )
    elif len(unique_skills) < 4:
        suggestions.append(
            "List relevant skills clearly and ensure they reflect your actual abilities."
        )

    # 4. Education: presence and descriptive content.
    education_content = section_has_content("education")

    if sections_found["education"] and education_content:
        education_score = 100
    elif sections_found["education"]:
        education_score = 50
    else:
        education_score = 0
        suggestions.append(
            "Add a clearly labelled Education section if applicable."
        )

    
    
    # 5. Professional experience. Projects do not count as employment.
    experience_heading_positions = [
        index
        for index, section, _ in headings
        if section == "experience"
    ]

    experience_lines = []

    for heading_index in experience_heading_positions:
        next_heading_index = next(
            (
                index
                for index, section, _ in headings
                if index > heading_index
            ),
            len(lines),
        )
        experience_lines.extend(
            lines[heading_index + 1:next_heading_index]
        )

    experience_text = " ".join(experience_lines).lower()
    experience_score = 0

    role_pattern = (
        r"\b(intern|engineer|developer|analyst|researcher|"
        r"contributor|reviewer|employee|manager|mentee)\b"
    )
    action_pattern = (
        r"\b(developed|built|implemented|designed|improved|"
        r"led|shipped|maintained|contributed|delivered|created)\b"
    )
    outcome_pattern = (
        r"\b(reduced|increased|improved|achieved|saved|"
        r"optimized|optimised|launched|supported)\b"
    )

    if experience_text.strip():
        experience_score = 30

        if re.search(role_pattern, experience_text):
            experience_score += 20

        if re.search(action_pattern, experience_text):
            experience_score += 25

        if re.search(outcome_pattern, experience_text):
            experience_score += 25

    elif sections_found["experience"]:
        experience_score = 10

    if experience_score < 50:
        suggestions.append(
            "Describe relevant internships or employment with your role, "
            "responsibilities, technologies, and outcomes. If you are a "
            "fresher without employment experience, this may be normal."
        )


    # 6. Projects: evaluate evidence only inside the Projects section.

    projects_score = 0
    project_text = ""

    # Match project headings, including headings with a colon or extra spacing.
    project_heading_pattern = (
        r"(?im)^\s*(?:key projects|academic projects|personal projects|"
        r"technical projects|selected projects|relevant projects|"
        r"project experience|projects|project)\s*:?\s*$"
    )

    project_match = re.search(
        r"(?im)^\s*(?:key\s+projects|academic\s+projects|personal\s+projects|"
        r"technical\s+projects|selected\s+projects|relevant\s+projects|"
        r"project\s+experience|projects|project)\b[^\r\n]*",
        text
    )

    if project_match:
        remaining_text = text[project_match.end():]

        # Stop at the next recognized section heading.
        next_heading_pattern = (
            r"(?im)^\s*(?:summary|objective|profile|skills|technical skills|"
            r"education|experience|work experience|employment|"
            r"certifications|achievements|awards|publications|"
            r"interests|languages)\s*:?\s*$"
        )

        next_heading = re.search(next_heading_pattern, remaining_text)

        project_text = (
            remaining_text[:next_heading.start()]
            if next_heading
            else remaining_text
        ).strip()

    print("\n===== PROJECTS DEBUG =====")
    print("Project heading found:", bool(project_match))
    print("Sections detected:", sections_found.get("projects"))
    print("Project text length:", len(project_text))
    print("Project text preview:", repr(project_text[:1000]))
    print("==========================\n")

    if project_text:
        projects_score = 40

        technology_patterns = (
            r"\b(python|java|javascript|react|node|fastapi|django|"
            r"tensorflow|pytorch|opencv|sql|docker|golang|flask|"
            r"scikit-learn|machine learning|deep learning|streamlit|"
            r"html|css|c\+\+|yolov5|arduino|esp32)\b"
        )

        action_patterns = (
            r"\b(built|developed|implemented|designed|created|"
            r"engineered|deployed|integrated|trained|automated)\b"
        )

        outcome_patterns = (
            r"\b(improved|reduced|achieved|optimized|accuracy|"
            r"performance|users|increased|decreased|saved|"
            r"r²|f1[- ]score|precision|recall)\b"
        )

        if re.search(technology_patterns, project_text, re.IGNORECASE):
            projects_score += 20

        if re.search(action_patterns, project_text, re.IGNORECASE):
            projects_score += 20

        if re.search(outcome_patterns, project_text, re.IGNORECASE):
            projects_score += 20

        projects_score = min(100, projects_score)

    elif sections_found["projects"]:
        projects_score = 20

    if projects_score < 60:
        suggestions.append(
            "Improve the Projects section by describing technologies used, "
            "your contribution, and measurable results."
        )
       



    # 7. Achievement evidence.
    # A number alone is not an achievement.
    outcome_terms = (
        r"\b(?:improved|increased|decreased|reduced|achieved|"
        r"delivered|saved|optimized|optimised|outperformed|"
        r"raised|lowered|accelerated)\b"
    )
    metric_pattern = (
        r"\b\d+(?:\.\d+)?\s*%"
        r"|\b\d+(?:\.\d+)?\s*(?:x|times)\b"
        r"|\b(?:accuracy|precision|recall|f1|r2|"
        r"users|customers|records|requests)\b"
    )

    quantified_evidence = bool(
        re.search(outcome_terms, text, flags=re.IGNORECASE)
        and re.search(metric_pattern, text, flags=re.IGNORECASE)
    )

    achievement_content = section_has_content("achievements")

    if achievement_content and quantified_evidence:
        achievement_score = 100
    elif achievement_content:
        achievement_score = 70
    elif quantified_evidence:
        achievement_score = 50
    else:
        achievement_score = 30

    if achievement_score < 70:
        suggestions.append(
            "Where accurate, describe outcomes and their context, such as "
            "model evaluation results, scale, or measurable improvements."
        )

    # 8. Extracted text sufficiency.
    # This is not a visual layout or true readability measurement.
    if word_count < 100:
        text_score = 20
        warnings.append(
            "Very little text was extracted. Check the PDF or whether OCR is needed."
        )
    elif word_count < 200:
        text_score = 50
        warnings.append(
            "Relatively little text was extracted. Check for missing resume content."
        )
    elif word_count <= 900:
        text_score = 100
    else:
        text_score = 80
        warnings.append(
            "A large amount of text was extracted. Review for unnecessary repetition."
        )

    # Transparent fixed weights; weights sum to 100.
    weights = {
        "section_completeness": 0.15,
        "contact_information": 0.10,
        "skills_evidence": 0.15,
        "education_evidence": 0.10,
        "experience_evidence": 0.15,
        "projects_evidence": 0.15,
        "quantified_achievements": 0.10,
        "text_sufficiency": 0.10,
    }

    component_scores = {
        "section_completeness": section_score,
        "contact_information": contact_score,
        "skills_evidence": skills_score,
        "education_evidence": education_score,
        "experience_evidence": experience_score,
        "projects_evidence": projects_score,
        "quantified_achievements": achievement_score,
        "text_sufficiency": text_score,
    }

    overall_score = round(sum(
        component_scores[name] * weight
        for name, weight in weights.items()
    ))

    if not sections_found["summary"]:
        suggestions.append(
            "Consider adding a concise professional summary or career objective."
        )

    if not sections_found["certifications"]:
        suggestions.append(
            "Add relevant certifications if you have them; do not list unearned certificates."
        )

    if not suggestions:
        suggestions.append(
            "Review the resume for accuracy, relevance, and evidence supporting your claims."
        )

    
    return {
        "ats_score": overall_score,
        "score_type": "Estimated general ATS readiness",
        "score_breakdown": component_scores,
        "word_count": word_count,
        "skills_detected": unique_skills,
        "sections_found": sections_found,
        "sections_with_content": sections_with_content,
        "warnings": warnings,
        "suggestions": list(dict.fromkeys(suggestions)),
        "disclaimer": (
            "This is a rule-based estimate from extracted resume text. "
            "It is not an official ATS score, does not measure visual PDF layout, "
            "and does not predict hiring outcomes or job-specific compatibility."
        ),
    }


