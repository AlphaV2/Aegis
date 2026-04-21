from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import WalletFundIn, WalletOut
from app.services.audit_service import log_event


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.post("/fund", response_model=WalletOut)
async def fund_wallet(payload: WalletFundIn, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Wallet).where(Wallet.agent_id == payload.agent_id).with_for_update())
    wallet = q.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    wallet.balance = wallet.balance + payload.amount
    await log_event(db, "WALLET_FUNDED", {"agent_id": str(payload.agent_id), "amount": str(payload.amount)})
    await db.commit()
    await db.refresh(wallet)
    return wallet


@router.get("/{agent_id}", response_model=WalletOut)
async def get_balance(agent_id: str, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Wallet).where(Wallet.agent_id == agent_id))
    wallet = q.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
