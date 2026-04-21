from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import Agent
from app.models.wallet import Wallet
from app.models.policy import Policy
from app.models.transaction import Transaction
from app.schemas.spend import SpendIn
from app.services.audit_service import log_event
from app.services.policy_engine import evaluate_policy
from app.services.payment_adapter import payment_adapter


async def execute_spend(db: AsyncSession, agent: Agent, payload: SpendIn) -> Transaction:
    existing = await db.execute(
        select(Transaction).where(
            Transaction.agent_id == payload.agent_id,
            Transaction.idempotency_key == payload.idempotency_key,
        )
    )
    existing_tx = existing.scalar_one_or_none()
    if existing_tx:
        if Decimal(existing_tx.amount) != payload.amount or existing_tx.vendor != payload.vendor:
            raise HTTPException(status_code=409, detail="Idempotency key conflict")
        return existing_tx

    wallet_q = await db.execute(
        select(Wallet).where(Wallet.agent_id == payload.agent_id).with_for_update()
    )
    wallet = wallet_q.scalar_one_or_none()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    policy_q = await db.execute(
        select(Policy).where(Policy.agent_id == payload.agent_id).with_for_update()
    )
    policy = policy_q.scalar_one_or_none()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    decision = await evaluate_policy(db, policy, payload.agent_id, payload.amount, payload.vendor, payload.category)

    tx = Transaction(
        agent_id=payload.agent_id,
        amount=payload.amount,
        vendor=payload.vendor.strip(),
        category=payload.category.strip().lower(),
        status=decision.status,
        reason=decision.reason,
        idempotency_key=payload.idempotency_key,
    )

    await log_event(db, "SPEND_ATTEMPT", {
        "agent_id": str(agent.id),
        "amount": str(payload.amount),
        "vendor": payload.vendor,
        "idempotency_key": payload.idempotency_key,
    })

    if decision.status == "APPROVED":
        if Decimal(wallet.balance) < payload.amount:
            tx.status = "REJECTED"
            tx.reason = "insufficient_balance"
            db.add(tx)
            await log_event(db, "SPEND_REJECTED", {"reason": tx.reason, "agent_id": str(agent.id)})
            return tx

        wallet.balance = Decimal(wallet.balance) - payload.amount
        result = await payment_adapter.charge(float(payload.amount), payload.vendor)
        if result.get("status") != "SUCCESS":
            raise HTTPException(status_code=502, detail="Payment adapter failure")
        await log_event(db, "PAYMENT_SUCCESS", {"agent_id": str(agent.id), "result": result})

    if decision.status == "REJECTED":
        await log_event(db, "SPEND_REJECTED", {"reason": decision.reason, "agent_id": str(agent.id)})

    if decision.status == "PENDING_APPROVAL":
        await log_event(db, "SPEND_PENDING", {"reason": decision.reason, "agent_id": str(agent.id)})

    db.add(tx)
    return tx
