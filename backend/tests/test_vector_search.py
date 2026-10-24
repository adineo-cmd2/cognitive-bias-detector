from app.services.embedder import cosine, embed
from app.services.vector_store import search


def test_duplicate_ranks_first():
    a = "I always knew I was right about the market trend."
    b = "The gauge rose 12% after calibration of the sensor array."
    va = embed(a)
    vb = embed(b)
    assert len(va) == 128
    assert len(vb) == 128
    # self-similarity ~1.0
    assert abs(cosine(va, va) - 1.0) < 1e-6
    items = [
        {"id": "a", "embedding": va},
        {"id": "b", "embedding": vb},
    ]
    results = search(va, items, k=2)
    assert results[0]["id"] == "a"
    assert len(results) == 2
