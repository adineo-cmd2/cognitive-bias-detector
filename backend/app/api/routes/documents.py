from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.ingestion_pipeline import ingest

router = APIRouter()

_ALLOWED = {".txt", ".md", ".pdf"}


def _extract_text(filename: str, raw: bytes) -> str:
    lower = (filename or "").lower()
    if lower.endswith(".pdf"):
        from pypdf import PdfReader
        from io import BytesIO

        reader = PdfReader(BytesIO(raw))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    return raw.decode("utf-8", errors="ignore")


@router.post("/upload")
def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    name = file.filename or ""
    if not any(name.lower().endswith(ext) for ext in _ALLOWED):
        raise HTTPException(status_code=400, detail="bad file type (use .txt/.md/.pdf)")
    raw = file.file.read()
    text = _extract_text(name, raw)
    document_id = ingest(db, user, name, text)
    chunks = (
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()
    )
    biases_found = (
        db.query(BiasRecord).filter(BiasRecord.document_id == document_id).count()
    )
    return {"document_id": document_id, "chunks": chunks, "biases_found": biases_found}


@router.get("")
def list_documents(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    docs = (
        db.query(Document)
        .filter(Document.user_id == user.id)
        .order_by(Document.id)
        .all()
    )
    out = []
    for d in docs:
        chunks = (
            db.query(DocumentChunk).filter(DocumentChunk.document_id == d.id).count()
        )
        biases = (
            db.query(BiasRecord).filter(BiasRecord.document_id == d.id).count()
        )
        out.append(
            {
                "id": d.id,
                "filename": d.filename,
                "chunks": chunks,
                "biases": biases,
                "created_at": d.created_at.isoformat() if d.created_at else None,
            }
        )
    return out


@router.delete("")
def delete_all_documents(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    doc_ids = [
        row[0]
        for row in db.query(Document.id).filter(Document.user_id == user.id).all()
    ]
    if doc_ids:
        db.query(BiasRecord).filter(BiasRecord.document_id.in_(doc_ids)).delete(
            synchronize_session=False
        )
        db.query(DocumentChunk).filter(DocumentChunk.document_id.in_(doc_ids)).delete(
            synchronize_session=False
        )
        db.query(Document).filter(Document.id.in_(doc_ids)).delete(
            synchronize_session=False
        )
        db.commit()
    return {"deleted_documents": len(doc_ids)}


@router.delete("/{doc_id}")
def delete_document(
    doc_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.user_id == user.id)
        .first()
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="document not found")
    db.query(BiasRecord).filter(BiasRecord.document_id == doc.id).delete()
    db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()
    db.delete(doc)
    db.commit()
    return {"ok": True}
