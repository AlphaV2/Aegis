from decimal import Decimal

import pytest
from sqlalchemy import select

from app.models.policy import Policy
from app.services.policy_engine import evaluate_policy


@pytest.mark.asyncio
async def test_policy_rejects_vendor_not_allowed(db_session, seeded_agent):
    policy = (await db_session.execute(select(Policy).where(Policy.agent_id == seeded_agent.id))).scalar_one()

    decision = await evaluate_policy(
        db_session,
        policy,
        seeded_agent.id,
        Decimal("100.00"),
        "unknown",
        "infra",
    )
    assert decision.status == "REJECTED"
    assert decision.reason == "vendor_not_allowed"


@pytest.mark.asyncio
async def test_policy_returns_pending_above_threshold(db_session, seeded_agent):
    policy = (await db_session.execute(select(Policy).where(Policy.agent_id == seeded_agent.id))).scalar_one()

    decision = await evaluate_policy(
        db_session,
        policy,
        seeded_agent.id,
        Decimal("350.00"),
        "openai",
        "infra",
    )
    assert decision.status == "PENDING_APPROVAL"
    assert decision.reason == "amount_requires_approval"


@pytest.mark.asyncio
async def test_policy_approves_valid_spend(db_session, seeded_agent):
    policy = (await db_session.execute(select(Policy).where(Policy.agent_id == seeded_agent.id))).scalar_one()

    decision = await evaluate_policy(
        db_session,
        policy,
        seeded_agent.id,
        Decimal("120.00"),
        "openai",
        "infra",
    )
    assert decision.status == "APPROVED"
    assert decision.reason == "policy_passed"
