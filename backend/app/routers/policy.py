from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.policy import Policy
from app.schemas.policy import PolicySetIn, PolicyOut
from app.services.audit_service import log_event


router = APIRouter(prefix="/policy", tags=["policy"])


@router.post("/set", response_model=PolicyOut)
async def set_policy(payload: PolicySetIn, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Policy).where(Policy.agent_id == payload.agent_id).with_for_update())
    policy = q.scalar_one_or_none()

    normalized_vendors = [v.strip().lower() for v in payload.allowed_vendors]
    normalized_categories = [c.strip().lower() for c in payload.blocked_categories]

    if policy:
        policy.per_tx_limit = payload.per_tx_limit
        policy.daily_limit = payload.daily_limit
        policy.monthly_limit = payload.monthly_limit
        policy.allowed_vendors = normalized_vendors
        policy.blocked_categories = normalized_categories
        policy.requires_approval_above = payload.requires_approval_above
    else:
        policy = Policy(
            agent_id=payload.agent_id,
            per_tx_limit=payload.per_tx_limit,
            daily_limit=payload.daily_limit,
            monthly_limit=payload.monthly_limit,
            allowed_vendors=normalized_vendors,
            blocked_categories=normalized_categories,
            requires_approval_above=payload.requires_approval_above,
        )
        db.add(policy)

    await log_event(db, "POLICY_SET", {"agent_id": str(payload.agent_id)})
    await db.commit()
    await db.refresh(policy)
    return policy
