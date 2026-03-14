from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import DateTime, JSON, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import ContentType, ProcessingStatus, SourcePlatform


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    source_url: Mapped[str] = mapped_column(Text, unique=True, index=True)
    source_platform: Mapped[str] = mapped_column(default=SourcePlatform.GENERIC_WEB.value)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    short_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    keywords: Mapped[list[str]] = mapped_column(JSON, default=list)
    category: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    content_type: Mapped[str | None] = mapped_column(Text, default=ContentType.UNKNOWN.value)
    processing_status: Mapped[str] = mapped_column(default=ProcessingStatus.READY.value)
    search_document: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

