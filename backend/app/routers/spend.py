from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_agent, verify_signed_request, check_rate_limit, check_velocity
from app.models.agent import Agent
from app.schemas.spend import SpendIn, SpendOut
from app.services.spend_service import execute_spend


router = APIRouter(prefix="/spend", tags=["spend"])


@router.post("", response_model=SpendOut, dependencies=[Depends(verify_signed_request), Depends(check_rate_limit), Depends(check_velocity)])
async def spend(
    payload: SpendIn,
    agent: Agent = Depends(get_current_agent),
    db: AsyncSession = Depends(get_db),
):
    if payload.agent_id != agent.id:
        raise HTTPException(status_code=403, detail="agent_id does not match API key")

    tx = await execute_spend(db, agent, payload)
    await db.commit()
    return SpendOut(transaction_id=tx.id, status=tx.status, reason=tx.reason)
