from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.crypto import decrypt_text
from app.db.session import get_db
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.embedder import cosine, embed

router = APIRouter()


@router.get("")
def search(
    q: str = "",
    k: int = 8,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    chunks = (
        db.query(DocumentChunk, Document)
        .join(Document, DocumentChunk.document_id == Document.id)
        .filter(Document.user_id == user.id)
        .order_by(DocumentChunk.id)
        .all()
    )
    query_vec = embed(q or "")
    scored = []
    for chunk, doc in chunks:
        score = cosine(query_vec, chunk.embedding or [])
        scored.append((score, chunk, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    results = []
    for score, chunk, doc in scored[: max(0, k)]:
        biases = (
            db.query(BiasRecord).filter(BiasRecord.chunk_id == chunk.id).all()
        )
        results.append(
            {
                "chunk_id": chunk.id,
                "document": doc.filename,
                "snippet": decrypt_text(chunk.text_enc),
                "score": score,
                "biases": [b.bias_type for b in biases],
            }
        )
    return {"results": results}
