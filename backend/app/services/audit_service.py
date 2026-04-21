from app.models.audit_log import AuditLog
from sqlalchemy.ext.asyncio import AsyncSession


async def log_event(db: AsyncSession, event_type: str, payload: dict) -> None:
    db.add(AuditLog(event_type=event_type, payload=payload))
