from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Float, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BiasRecord(Base):
    __tablename__ = "bias_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"), index=True)
    chunk_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_chunks.id"), index=True)
    bias_type: Mapped[str] = mapped_column(String(100))
    quote: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    explanation: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
