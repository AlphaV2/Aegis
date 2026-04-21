from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.audit_log import AuditLog


router = APIRouter(prefix="/audit-logs", tags=["audit"])


@router.get("")
async def list_audit_logs(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(300))
    rows = q.scalars().all()
    return [
        {
            "id": str(r.id),
            "event_type": r.event_type,
            "payload": r.payload,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in rows
    ]
