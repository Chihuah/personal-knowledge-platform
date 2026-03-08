from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    knowledge_item_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("knowledge_items.id", ondelete="CASCADE"),
        index=True,
    )
    action: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    knowledge_item = relationship("KnowledgeItem", back_populates="ingestion_logs")
