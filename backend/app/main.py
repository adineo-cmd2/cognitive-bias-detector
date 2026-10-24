from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analytics, documents, profile, search
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

import app.models.user  # noqa: F401 register tables
import app.models.document  # noqa: F401
import app.models.document_chunk  # noqa: F401
import app.models.bias_record  # noqa: F401

Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title="Cognitive Bias Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:4322"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"ok": True}


app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
