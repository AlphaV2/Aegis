from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict


class PolicySetIn(BaseModel):
    agent_id: UUID
    per_tx_limit: Decimal = Field(ge=0)
    daily_limit: Decimal = Field(ge=0)
    monthly_limit: Decimal = Field(ge=0)
    allowed_vendors: list[str] = Field(default_factory=list)
    blocked_categories: list[str] = Field(default_factory=list)
    requires_approval_above: Decimal = Field(ge=0)


class PolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    agent_id: UUID
    per_tx_limit: Decimal
    daily_limit: Decimal
    monthly_limit: Decimal
    allowed_vendors: list[str]
    blocked_categories: list[str]
    requires_approval_above: Decimal
