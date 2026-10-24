"""Smoke: upload txt -> bias-map -> search -> trend (no auth, single local user)."""

from fastapi.testclient import TestClient

from app.main import app


def test_api_smoke():
    c = TestClient(app)

    r = c.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

    text = (
        "I always knew I was right about this market call. "
        "This confirms what I believed all along, and I only trust "
        "sources that agree with my view."
    )
    r = c.post(
        "/api/documents/upload",
        files={"file": ("notes.txt", text.encode("utf-8"), "text/plain")},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["chunks"] >= 1
    assert body["biases_found"] >= 1
    doc_id = body["document_id"]

    r = c.get("/api/documents")
    assert r.status_code == 200
    docs = r.json()
    assert any(d["id"] == doc_id for d in docs)

    r = c.get("/api/profile/bias-map")
    assert r.status_code == 200
    ranked = r.json()["ranked"]
    assert len(ranked) > 0
    assert ranked[0]["count"] >= 1

    r = c.get("/api/search", params={"q": "I always knew I was right", "k": 5})
    assert r.status_code == 200
    results = r.json()["results"]
    assert len(results) >= 1
    assert "always knew" in results[0]["snippet"].lower()

    r = c.get("/api/analytics/trend")
    assert r.status_code == 200
    assert isinstance(r.json()["trend"], list)

    r = c.get("/api/analytics/cooccurrence")
    assert r.status_code == 200

    r = c.delete(f"/api/documents/{doc_id}")
    assert r.status_code == 200


def test_delete_all_documents():
    c = TestClient(app)

    # Clear any leftover state from other tests (single shared local user).
    r = c.delete("/api/documents")
    assert r.status_code == 200

    texts = [
        "I always knew I was right about this market call. This confirms it.",
        "I have already invested so much time that I cannot quit this failing plan now.",
    ]
    for i, text in enumerate(texts):
        r = c.post(
            "/api/documents/upload",
            files={"file": (f"wipe-{i}.txt", text.encode("utf-8"), "text/plain")},
        )
        assert r.status_code == 200

    r = c.get("/api/documents")
    assert r.status_code == 200
    assert len(r.json()) == 2

    r = c.delete("/api/documents")
    assert r.status_code == 200
    assert r.json()["deleted_documents"] == 2

    r = c.get("/api/documents")
    assert r.status_code == 200
    assert r.json() == []

    r = c.get("/api/profile/bias-map")
    assert r.status_code == 200
    assert r.json()["ranked"] == []
    assert r.json()["radar"] == []
