from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.transaction import Transaction


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("")
async def list_transactions(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Transaction).order_by(Transaction.created_at.desc()).limit(200))
    rows = q.scalars().all()
    return [
        {
            "id": str(t.id),
            "agent_id": str(t.agent_id),
            "amount": str(t.amount),
            "vendor": t.vendor,
            "category": t.category,
            "status": t.status,
            "reason": t.reason,
            "idempotency_key": t.idempotency_key,
            "created_at": t.created_at.isoformat(),
        }
        for t in rows
    ]
