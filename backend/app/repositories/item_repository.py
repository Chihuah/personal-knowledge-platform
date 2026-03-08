from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session

from app.models.enums import ProcessingStatus
from app.models.ingestion_log import IngestionLog
from app.models.knowledge_item import KnowledgeItem


@dataclass
class ItemListResult:
    items: Sequence[KnowledgeItem]
    total: int


class KnowledgeItemRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_url(self, source_url: str) -> KnowledgeItem | None:
        return self.session.scalar(
            select(KnowledgeItem).where(KnowledgeItem.source_url == source_url)
        )

    def get_by_id(self, item_id: UUID) -> KnowledgeItem | None:
        return self.session.get(KnowledgeItem, item_id)

    def add(self, item: KnowledgeItem) -> KnowledgeItem:
        self.session.add(item)
        self.session.flush()
        return item

    def list_items(
        self,
        *,
        query: str | None = None,
        platform: str | None = None,
        category: str | None = None,
        status: str | None = None,
        content_type: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
        sort: str = "newest",
    ) -> ItemListResult:
        stmt = select(KnowledgeItem)

        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    KnowledgeItem.source_url.ilike(pattern),
                    KnowledgeItem.title.ilike(pattern),
                    KnowledgeItem.short_summary.ilike(pattern),
                    KnowledgeItem.cleaned_content.ilike(pattern),
                    KnowledgeItem.search_document.ilike(pattern),
                    cast(KnowledgeItem.keywords, String).ilike(pattern),
                )
            )

        if platform:
            stmt = stmt.where(KnowledgeItem.source_platform == platform)
        if category:
            stmt = stmt.where(KnowledgeItem.category == category)
        if status:
            stmt = stmt.where(KnowledgeItem.processing_status == status)
        if content_type:
            stmt = stmt.where(KnowledgeItem.content_type == content_type)
        if date_from:
            stmt = stmt.where(KnowledgeItem.captured_at >= date_from)
        if date_to:
            stmt = stmt.where(KnowledgeItem.captured_at <= date_to)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.scalar(count_stmt) or 0

        order_column = KnowledgeItem.captured_at.desc()
        if sort == "oldest":
            order_column = KnowledgeItem.captured_at.asc()
        elif sort == "updated":
            order_column = KnowledgeItem.updated_at.desc()

        items = self.session.scalars(
            stmt.order_by(order_column)
            .offset((page - 1) * page_size)
            .limit(page_size)
        ).all()
        return ItemListResult(items=items, total=total)

    def latest_items(self, limit: int = 5) -> Sequence[KnowledgeItem]:
        return self.session.scalars(
            select(KnowledgeItem)
            .order_by(KnowledgeItem.captured_at.desc())
            .limit(limit)
        ).all()

    def list_failed_items(self, limit: int = 5) -> Sequence[KnowledgeItem]:
        return self.session.scalars(
            select(KnowledgeItem)
            .where(KnowledgeItem.processing_status == ProcessingStatus.FAILED.value)
            .order_by(KnowledgeItem.updated_at.desc())
            .limit(limit)
        ).all()

    def get_dashboard(self) -> dict[str, object]:
        total_count = self.session.scalar(select(func.count(KnowledgeItem.id))) or 0
        recent_threshold = datetime.now(timezone.utc) - timedelta(days=7)
        recent_count = self.session.scalar(
            select(func.count(KnowledgeItem.id)).where(
                KnowledgeItem.captured_at >= recent_threshold
            )
        ) or 0

        category_distribution = self.session.execute(
            select(KnowledgeItem.category, func.count(KnowledgeItem.id)).group_by(
                KnowledgeItem.category
            )
        ).all()
        status_distribution = self.session.execute(
            select(KnowledgeItem.processing_status, func.count(KnowledgeItem.id)).group_by(
                KnowledgeItem.processing_status
            )
        ).all()

        return {
            "total_count": total_count,
            "recent_count": recent_count,
            "latest_items": self.latest_items(limit=5),
            "failed_items": self.list_failed_items(limit=5),
            "category_distribution": [
                {"label": label or "uncategorized", "count": count}
                for label, count in category_distribution
            ],
            "status_distribution": [
                {"label": label, "count": count}
                for label, count in status_distribution
            ],
        }

    def add_log(
        self,
        *,
        knowledge_item_id: UUID,
        action: str,
        status: str,
        message: str | None = None,
    ) -> IngestionLog:
        log = IngestionLog(
            knowledge_item_id=knowledge_item_id,
            action=action,
            status=status,
            message=message,
        )
        self.session.add(log)
        self.session.flush()
        return log

    def update_status(self, item: KnowledgeItem, status: ProcessingStatus) -> None:
        item.processing_status = status.value
        item.updated_at = datetime.now(timezone.utc)

    def rebuild_search_document(self, item: KnowledgeItem) -> None:
        keywords_text = " ".join(item.keywords or [])
        parts = [
            item.title or "",
            item.description or "",
            item.short_summary or "",
            item.full_summary or "",
            item.cleaned_content or "",
            keywords_text,
            item.category or "",
        ]
        item.search_document = "\n".join(part for part in parts if part).strip() or None

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, item: KnowledgeItem) -> None:
        self.session.refresh(item)
