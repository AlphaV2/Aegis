import asyncio
from decimal import Decimal

from sqlalchemy import select

from app.database import SessionLocal
from app.models.agent import Agent
from app.models.wallet import Wallet
from app.models.policy import Policy
from app.utils.security import generate_api_key, hash_api_key


async def seed() -> None:
    async with SessionLocal() as db:
        q = await db.execute(select(Agent).where(Agent.name == "demo-agent"))
        existing = q.scalar_one_or_none()
        if existing:
            print("demo-agent already exists")
            return

        key = generate_api_key()
        agent = Agent(name="demo-agent", api_key_hash=hash_api_key(key), status="ACTIVE")
        db.add(agent)
        await db.flush()

        db.add(Wallet(agent_id=agent.id, balance=Decimal("5000.00"), currency="USD"))
        db.add(
            Policy(
                agent_id=agent.id,
                per_tx_limit=Decimal("1000.00"),
                daily_limit=Decimal("3000.00"),
                monthly_limit=Decimal("15000.00"),
                allowed_vendors=["openai", "aws", "supabase"],
                blocked_categories=["gambling", "adult"],
                requires_approval_above=Decimal("700.00"),
            )
        )

        await db.commit()
        print(f"seeded agent_id={agent.id}")
        print(f"api_key={key}")


if __name__ == "__main__":
    asyncio.run(seed())
