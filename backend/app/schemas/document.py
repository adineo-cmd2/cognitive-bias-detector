from datetime import datetime

from pydantic import BaseModel


class DocumentOut(BaseModel):
    id: int
    filename: str
    created_at: datetime

    class Config:
        from_attributes = True


class BiasRecordOut(BaseModel):
    id: int
    document_id: int
    chunk_id: int
    bias_type: str
    quote: str
    confidence: float
    explanation: str

    class Config:
        from_attributes = True
