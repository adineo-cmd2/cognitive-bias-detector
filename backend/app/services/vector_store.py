"""Cosine top-k search over stored chunk embeddings."""

from app.services.embedder import cosine


def search(
    query_vec: list[float], items: list[dict], k: int = 8
) -> list[dict]:
    scored = []
    for item in items:
        emb = item.get("embedding") or []
        scored.append((cosine(query_vec, emb), item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = scored[: max(0, k)]
    return [{"id": item.get("id"), "score": score} for score, item in top]
