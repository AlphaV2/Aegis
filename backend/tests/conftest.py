import os

import pytest_asyncio
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@localhost:5432/aegis"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

from app.database import Base
from app.models.agent import Agent
from app.models.wallet import Wallet
from app.models.policy import Policy
from app.utils.security import generate_api_key, hash_api_key


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def seeded_agent(db_session):
    raw_key = generate_api_key()
    agent = Agent(name="test-agent", api_key_hash=hash_api_key(raw_key), status="ACTIVE")
    db_session.add(agent)
    await db_session.flush()

    wallet = Wallet(agent_id=agent.id, balance=Decimal("1000.00"), currency="USD")
    policy = Policy(
        agent_id=agent.id,
        per_tx_limit=Decimal("500.00"),
        daily_limit=Decimal("1500.00"),
        monthly_limit=Decimal("5000.00"),
        allowed_vendors=["openai", "aws"],
        blocked_categories=["gambling"],
        requires_approval_above=Decimal("300.00"),
    )

    db_session.add(wallet)
    db_session.add(policy)
    await db_session.commit()

    return agent
