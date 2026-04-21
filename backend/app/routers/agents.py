from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.agent import Agent
from app.models.wallet import Wallet
from app.schemas.agent import AgentCreateIn, AgentCreateOut, AgentOut
from app.services.audit_service import log_event
from app.utils.security import generate_api_key, hash_api_key


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentCreateOut)
async def create_agent(payload: AgentCreateIn, db: AsyncSession = Depends(get_db)):
    raw_key = generate_api_key()
    agent = Agent(name=payload.name.strip(), api_key_hash=hash_api_key(raw_key), status="ACTIVE")
    db.add(agent)
    await db.flush()

    wallet = Wallet(agent_id=agent.id, balance=0, currency="USD")
    db.add(wallet)

    await log_event(db, "AGENT_CREATED", {"agent_id": str(agent.id), "name": agent.name})
    await db.commit()
    await db.refresh(agent)

    return AgentCreateOut(agent=AgentOut.model_validate(agent), api_key=raw_key)


@router.get("")
async def list_agents(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Agent, Wallet).join(Wallet, Wallet.agent_id == Agent.id, isouter=True))
    rows = q.all()
    return [
        {
            "id": str(agent.id),
            "name": agent.name,
            "status": agent.status,
            "created_at": agent.created_at.isoformat(),
            "wallet_balance": str(wallet.balance) if wallet else "0.00",
            "currency": wallet.currency if wallet else "USD",
        }
        for agent, wallet in rows
    ]
