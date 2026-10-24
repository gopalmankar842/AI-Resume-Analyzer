
from functools import lru_cache
from sklearn.metrics.pairwise import cosine_similarity


@lru_cache(maxsize=1)
def get_model():
    # Import PyTorch-backed model only when needed.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        "all-MiniLM-L6-v2",
        device="cpu"
    )


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str
) -> float:
    model = get_model()

    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    percentage = float(similarity) * 100
    percentage = max(0.0, min(100.0, percentage))

    return round(percentage, 2)
