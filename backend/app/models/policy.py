import uuid
from sqlalchemy import Numeric, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, unique=True)

    per_tx_limit: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    daily_limit: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    monthly_limit: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)
    allowed_vendors: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    blocked_categories: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    requires_approval_above: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0)

    agent = relationship("Agent", back_populates="policy")
