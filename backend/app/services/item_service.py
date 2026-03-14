from datetime import datetime
from uuid import UUID

from app.models.knowledge_item import KnowledgeItem
from app.repositories.item_repository import (
    KnowledgeItemRepository,
    ItemListResult,
    ItemNotFoundError,
)
from app.schemas.items import IngestItemRequest


class ItemService:
    def __init__(self, repository: KnowledgeItemRepository) -> None:
        self.repository = repository

    def ingest_item(self, payload: IngestItemRequest) -> tuple[KnowledgeItem, bool]:
        """Create or update a knowledge item from external ingestion.
        Returns (item, created) tuple.
        """
        existing = self.repository.get_by_url(payload.source_url)
        if existing:
            # Update existing item
            existing.source_platform = payload.source_platform
            existing.author = payload.author
            existing.published_at = payload.published_at
            existing.title = payload.title
            existing.short_summary = payload.short_summary
            existing.full_summary = payload.full_summary
            existing.keywords = payload.keywords
            existing.category = payload.category
            existing.content_type = payload.content_type
            existing.raw_content = payload.raw_content
            existing.processing_status = "ready"
            self.repository.rebuild_search_document(existing)
            self.repository.commit()
            self.repository.refresh(existing)
            return existing, False

        item = KnowledgeItem(
            source_url=payload.source_url,
            source_platform=payload.source_platform,
            author=payload.author,
            published_at=payload.published_at,
            title=payload.title,
            short_summary=payload.short_summary,
            full_summary=payload.full_summary,
            keywords=payload.keywords,
            category=payload.category,
            content_type=payload.content_type,
            raw_content=payload.raw_content,
            processing_status="ready",
        )
        self.repository.create(item)
        self.repository.rebuild_search_document(item)
        self.repository.commit()
        self.repository.refresh(item)
        return item, True

    def get_item(self, item_id: UUID) -> KnowledgeItem:
        return self.repository.get_by_id(item_id)

    def list_items(self, **kwargs) -> ItemListResult:
        return self.repository.list_items(**kwargs)

    def get_dashboard(self) -> dict:
        return self.repository.get_dashboard_data()

    def get_categories(self) -> list[str]:
        return self.repository.get_all_categories()

    @staticmethod
    def parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except (ValueError, TypeError):
            return None
