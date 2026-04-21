from typing import Optional

from fastapi import Header, HTTPException, Depends, Request
from redis.asyncio import from_url as redis_from_url
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.agent import Agent
from app.utils.security import hash_api_key, verify_hmac_signature, timestamp_is_fresh


redis_client = redis_from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=0.1,
    socket_timeout=0.1,
    retry_on_timeout=False,
)


async def redis_get(key: str):
    return await redis_client.get(key)


async def redis_setex(key: str, ttl: int, value: str):
    return await redis_client.setex(key, ttl, value)


async def redis_incr(key: str):
    return await redis_client.incr(key)


async def redis_expire(key: str, ttl: int):
    return await redis_client.expire(key, ttl)


async def get_current_agent(
    x_api_key: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Agent:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")

    q = await db.execute(select(Agent).where(Agent.api_key_hash == hash_api_key(x_api_key)))
    agent = q.scalar_one_or_none()
    if not agent or agent.status != "ACTIVE":
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")
    return agent


async def verify_signed_request(
    request: Request,
    x_signature: Optional[str] = Header(default=None),
    x_timestamp: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None),
    agent: Agent = Depends(get_current_agent),
) -> None:
    if not x_signature or not x_timestamp:
        raise HTTPException(status_code=401, detail="Missing signature headers")

    if not timestamp_is_fresh(x_timestamp, settings.hmac_max_age_seconds):
        raise HTTPException(status_code=401, detail="Stale timestamp")

    replay_key = f"replay:{agent.id}:{x_signature}"
    if await redis_get(replay_key):
        raise HTTPException(status_code=409, detail="Replay detected")

    body = await request.body()
    canonical = f"{request.method}|{request.url.path}|{x_timestamp}|".encode("utf-8") + body

    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")

    if not verify_hmac_signature(canonical, x_signature, x_api_key):
        raise HTTPException(status_code=401, detail="Invalid signature")

    await redis_setex(replay_key, settings.hmac_max_age_seconds, "1")


async def check_rate_limit(agent: Agent = Depends(get_current_agent)) -> None:
    key = f"ratelimit:{agent.id}"
    count = await redis_incr(key)
    if count == 1:
        await redis_expire(key, 60)
    if count > settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


async def check_velocity(agent: Agent = Depends(get_current_agent)) -> None:
    key = f"velocity:{agent.id}"
    count = await redis_incr(key)
    if count == 1:
        await redis_expire(key, 300)
    if count > settings.velocity_limit_5_min:
        raise HTTPException(status_code=429, detail="Velocity threshold exceeded")
