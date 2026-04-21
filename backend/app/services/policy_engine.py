from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.policy import Policy
from app.models.transaction import Transaction


class PolicyDecision:
    def __init__(self, status: str, reason: str):
        self.status = status
        self.reason = reason


async def evaluate_policy(db: AsyncSession, policy: Policy, agent_id, amount: Decimal, vendor: str, category: str) -> PolicyDecision:
    vendor_n = vendor.strip().lower()
    category_n = category.strip().lower()

    if amount > Decimal(policy.per_tx_limit):
        return PolicyDecision("REJECTED", "per_tx_limit_exceeded")

    if policy.allowed_vendors and vendor_n not in [v.strip().lower() for v in policy.allowed_vendors]:
        return PolicyDecision("REJECTED", "vendor_not_allowed")

    if policy.blocked_categories and category_n in [c.strip().lower() for c in policy.blocked_categories]:
        return PolicyDecision("REJECTED", "category_blocked")

    now = datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    day_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.agent_id == agent_id,
            Transaction.status == "APPROVED",
            Transaction.created_at >= day_start,
        )
    )
    day_total = Decimal(day_q.scalar_one())

    month_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.agent_id == agent_id,
            Transaction.status == "APPROVED",
            Transaction.created_at >= month_start,
        )
    )
    month_total = Decimal(month_q.scalar_one())

    if day_total + amount > Decimal(policy.daily_limit):
        return PolicyDecision("REJECTED", "daily_limit_exceeded")

    if month_total + amount > Decimal(policy.monthly_limit):
        return PolicyDecision("REJECTED", "monthly_limit_exceeded")

    if amount > Decimal(policy.requires_approval_above):
        return PolicyDecision("PENDING_APPROVAL", "amount_requires_approval")

    return PolicyDecision("APPROVED", "policy_passed")
