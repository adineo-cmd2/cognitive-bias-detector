from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.user import User
from app.services import analytics_service

router = APIRouter()


def _own_records(db: Session, user_id: int) -> list[dict]:
    records = (
        db.query(BiasRecord)
        .join(Document, BiasRecord.document_id == Document.id)
        .filter(Document.user_id == user_id)
        .order_by(BiasRecord.id)
        .all()
    )
    return [
        {
            "bias_type": r.bias_type,
            "document_id": r.document_id,
            "created_at": r.created_at,
        }
        for r in records
    ]


@router.get("/trend")
def get_trend(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"trend": analytics_service.trend(_own_records(db, user.id))}


@router.get("/cooccurrence")
def get_cooccurrence(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return {"cooccurrence": analytics_service.cooccurrence(_own_records(db, user.id))}
