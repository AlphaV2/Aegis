from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class WalletFundIn(BaseModel):
    agent_id: UUID
    amount: Decimal = Field(gt=0)


class WalletOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    agent_id: UUID
    balance: Decimal
    currency: str
