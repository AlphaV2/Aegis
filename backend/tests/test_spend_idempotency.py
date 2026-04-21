from decimal import Decimal

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.schemas.spend import SpendIn
from app.services.spend_service import execute_spend


@pytest.mark.asyncio
async def test_spend_idempotent_duplicate_returns_same_transaction(db_session, seeded_agent):
    payload = SpendIn(
        agent_id=seeded_agent.id,
        amount=Decimal("120.00"),
        vendor="openai",
        category="infra",
        idempotency_key="idem_test_same",
    )

    tx1 = await execute_spend(db_session, seeded_agent, payload)
    db_session.add(tx1)
    await db_session.commit()

    tx2 = await execute_spend(db_session, seeded_agent, payload)
    assert tx1.id == tx2.id
    assert tx2.status == "APPROVED"


@pytest.mark.asyncio
async def test_spend_idempotency_conflict_on_payload_change(db_session, seeded_agent):
    first = SpendIn(
        agent_id=seeded_agent.id,
        amount=Decimal("120.00"),
        vendor="openai",
        category="infra",
        idempotency_key="idem_conflict",
    )
    await execute_spend(db_session, seeded_agent, first)
    await db_session.commit()

    changed = SpendIn(
        agent_id=seeded_agent.id,
        amount=Decimal("121.00"),
        vendor="openai",
        category="infra",
        idempotency_key="idem_conflict",
    )

    with pytest.raises(HTTPException) as exc:
        await execute_spend(db_session, seeded_agent, changed)

    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_spend_rejects_insufficient_balance(db_session, seeded_agent):
    wallet = (await db_session.execute(select(Wallet).where(Wallet.agent_id == seeded_agent.id))).scalar_one()
    wallet.balance = Decimal("100.00")
    await db_session.commit()

    payload = SpendIn(
        agent_id=seeded_agent.id,
        amount=Decimal("290.00"),
        vendor="openai",
        category="infra",
        idempotency_key="idem_insufficient",
    )

    tx = await execute_spend(db_session, seeded_agent, payload)
    await db_session.commit()

    assert tx.status == "REJECTED"
    assert tx.reason == "insufficient_balance"

    rows = (await db_session.execute(select(Transaction))).scalars().all()
    assert len(rows) >= 1
