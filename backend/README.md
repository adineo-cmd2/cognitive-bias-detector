# Cognitive Bias Detector — backend

Run from `backend/`:

```bash
pip install -r requirements.txt
cp .env.example .env   # optional; works with no keys (mock detection mode)
python3 -m uvicorn app.main:app --port 8002
```

Tests: `python3 -m pytest tests/ -v` (8 tests).
