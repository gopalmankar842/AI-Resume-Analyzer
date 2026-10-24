
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_model():
    """Load the model only when semantic matching is requested."""
    return SentenceTransformer(
        "all-MiniLM-L6-v2",
        device="cpu"
    )


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str
) -> float:
    model = get_model()

    resume_embedding = model.encode(
        [resume_text],
        convert_to_numpy=True
    )

    job_embedding = model.encode(
        [job_description],
        convert_to_numpy=True
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    percentage = float(similarity) * 100
    percentage = max(0.0, min(100.0, percentage))

    return round(percentage, 2)
