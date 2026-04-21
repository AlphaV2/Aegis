from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class AgentCreateIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class AgentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: str


class AgentCreateOut(BaseModel):
    agent: AgentOut
    api_key: str
