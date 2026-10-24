"""Ingestion: chunk -> encrypt -> embed -> detect -> persist."""

from sqlalchemy.orm import Session

from app.core.crypto import encrypt_text
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.bias_detector import detect_biases
from app.services.chunker import chunk_text
from app.services.embedder import embed


def ingest(db: Session, user: User, filename: str, text: str) -> int:
    """Persist a document and its chunks/bias records. Returns document_id."""
    doc = Document(user_id=user.id, filename=filename)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    chunks = chunk_text(text or "")
    for idx, chunk in enumerate(chunks):
        dc = DocumentChunk(
            document_id=doc.id,
            idx=idx,
            text_enc=encrypt_text(chunk),
            embedding=embed(chunk),
        )
        db.add(dc)
        db.commit()
        db.refresh(dc)
        # Rule-based detection; LLM confirm deferred (mock detector, Task 3).
        for found in detect_biases(chunk):
            db.add(
                BiasRecord(
                    document_id=doc.id,
                    chunk_id=dc.id,
                    bias_type=found["bias_type"],
                    quote=found["quote"],
                    confidence=found["confidence"],
                    explanation=found["explanation"],
                )
            )
    db.commit()
    return doc.id
