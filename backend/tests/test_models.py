from app.core.crypto import decrypt_text, encrypt_text
from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User


def test_user_doc_chunk_bias_link_and_crypto_roundtrip():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    u = User(email="bias@example.com", password_hash=hash_password("secret123"))
    db.add(u)
    db.commit()
    db.refresh(u)

    doc = Document(user_id=u.id, filename="notes.txt")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    assert doc.user_id == u.id

    raw = "I always knew I was right about this."
    chunk = DocumentChunk(
        document_id=doc.id, idx=0, text_enc=encrypt_text(raw), embedding=[0.1, 0.2]
    )
    db.add(chunk)
    db.commit()
    db.refresh(chunk)
    assert chunk.document_id == doc.id
    assert decrypt_text(chunk.text_enc) == raw

    bias = BiasRecord(
        document_id=doc.id,
        chunk_id=chunk.id,
        bias_type="confirmation_bias",
        quote=raw,
        confidence=0.7,
        explanation="Interprets evidence as confirmation.",
    )
    db.add(bias)
    db.commit()
    db.refresh(bias)
    assert bias.document_id == doc.id
    assert bias.chunk_id == chunk.id

    db.close()
