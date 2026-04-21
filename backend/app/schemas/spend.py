from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class SpendIn(BaseModel):
    agent_id: UUID
    amount: Decimal = Field(gt=0)
    vendor: str = Field(min_length=1, max_length=120)
    category: str = Field(default="general", min_length=1, max_length=80)
    idempotency_key: str = Field(min_length=8, max_length=120)


class SpendOut(BaseModel):
    transaction_id: UUID
    status: str
    reason: str
