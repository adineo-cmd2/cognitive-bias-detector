from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.bias_record import BiasRecord
from app.models.document import Document
from app.models.user import User

router = APIRouter()


@router.get("/bias-map")
def bias_map(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    records = (
        db.query(BiasRecord)
        .join(Document, BiasRecord.document_id == Document.id)
        .filter(Document.user_id == user.id)
        .order_by(BiasRecord.id)
        .all()
    )
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    for r in records:
        counts[r.bias_type] += 1
        examples.setdefault(r.bias_type, [])
        if len(examples[r.bias_type]) < 3:
            examples[r.bias_type].append(r.quote)
    ranked = [
        {"bias_type": bias_type, "count": count, "examples": examples[bias_type]}
        for bias_type, count in counts.most_common()
    ]
    radar = [{"bias_type": bias_type, "count": count} for bias_type, count in counts.most_common()]
    return {"ranked": ranked, "radar": radar}
