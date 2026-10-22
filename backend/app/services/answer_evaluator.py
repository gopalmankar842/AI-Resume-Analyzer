import re

from app.services.semantic_matcher import (
    calculate_semantic_similarity
)


def normalize_text(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def get_words(text: str) -> set:
    return set(
        normalize_text(text).split()
    )


def calculate_keyword_score(
    question: str,
    answer: str
) -> float:

    question_words = get_words(question)
    answer_words = get_words(answer)

    if not question_words:
        return 0.0

    common_words = question_words.intersection(
        answer_words
    )

    score = (
        len(common_words)
        / len(question_words)
    ) * 100

    return round(
        min(score, 100),
        2
    )


def calculate_length_score(
    answer: str
) -> float:

    word_count = len(
        get_words(answer)
    )

    if word_count < 5:
        return 20.0

    if word_count < 15:
        return 50.0

    if word_count < 30:
        return 75.0

    return 100.0


def evaluate_answer(
    question: str,
    answer: str
) -> dict:

    if not answer or not answer.strip():

        return {
            "score": 0,
            "keyword_score": 0,
            "semantic_score": 0,
            "strengths": [],
            "improvements": [
                "Provide an answer to the question."
            ]
        }

    # -----------------------------
    # Keyword relevance
    # -----------------------------

    keyword_score = calculate_keyword_score(
        question,
        answer
    )

    # -----------------------------
    # Answer length/detail
    # -----------------------------

    length_score = calculate_length_score(
        answer
    )

    # -----------------------------
    # Semantic similarity
    # -----------------------------

    semantic_score = calculate_semantic_similarity(
        question,
        answer
    )

    # -----------------------------
    # Final score
    # -----------------------------

    final_percentage = (
        keyword_score * 0.30
        + semantic_score * 0.50
        + length_score * 0.20
    )

    final_score = round(
        final_percentage / 10,
        1
    )

    # -----------------------------
    # Strengths
    # -----------------------------

    strengths = []

    if keyword_score >= 60:
        strengths.append(
            "Your answer contains relevant keywords."
        )

    if semantic_score >= 60:
        strengths.append(
            "Your answer is semantically relevant to the question."
        )

    if length_score >= 75:
        strengths.append(
            "Your answer provides reasonable detail."
        )

    if not strengths:
        strengths.append(
            "You attempted to address the question."
        )

    # -----------------------------
    # Improvements
    # -----------------------------

    improvements = []

    if keyword_score < 50:
        improvements.append(
            "Include more concepts directly related to the question."
        )

    if semantic_score < 60:
        improvements.append(
            "Make your explanation more directly connected to the question."
        )

    if length_score < 75:
        improvements.append(
            "Provide a more detailed explanation."
        )

    if not improvements:
        improvements.append(
            "Add a practical example to make your answer stronger."
        )

    return {
        "score": final_score,
        "keyword_score": round(keyword_score, 2),
        "semantic_score": round(semantic_score, 2),
        "strengths": strengths,
        "improvements": improvements
    }