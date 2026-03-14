from datetime import datetime, timezone, timedelta
from uuid import UUID

from sqlalchemy import func, select, or_, desc, asc
from sqlalchemy.orm import Session

from app.models.knowledge_item import KnowledgeItem


class ItemListResult:
    def __init__(self, items: list[KnowledgeItem], total: int):
        self.items = items
        self.total = total


class ItemNotFoundError(Exception):
    pass


class KnowledgeItemRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, item_id: UUID) -> KnowledgeItem:
        item = self.session.get(KnowledgeItem, item_id)
        if item is None:
            raise ItemNotFoundError(f"Item {item_id} not found.")
        return item

    def get_by_url(self, url: str) -> KnowledgeItem | None:
        stmt = select(KnowledgeItem).where(KnowledgeItem.source_url == url)
        return self.session.execute(stmt).scalar_one_or_none()

    def create(self, item: KnowledgeItem) -> KnowledgeItem:
        self.session.add(item)
        self.session.flush()
        return item

    def list_items(
        self,
        *,
        query: str | None = None,
        platform: str | None = None,
        category: str | None = None,
        content_type: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        page: int = 1,
        page_size: int = 20,
        sort: str = "newest",
    ) -> ItemListResult:
        stmt = select(KnowledgeItem)
        count_stmt = select(func.count(KnowledgeItem.id))

        filters = []

        if query:
            pattern = f"%{query}%"
            text_filter = or_(
                KnowledgeItem.search_document.ilike(pattern),
                KnowledgeItem.title.ilike(pattern),
                KnowledgeItem.short_summary.ilike(pattern),
                KnowledgeItem.full_summary.ilike(pattern),
                KnowledgeItem.author.ilike(pattern),
                KnowledgeItem.category.ilike(pattern),
            )
            filters.append(text_filter)

        if platform:
            filters.append(KnowledgeItem.source_platform == platform)
        if category:
            filters.append(KnowledgeItem.category == category)
        if content_type:
            filters.append(KnowledgeItem.content_type == content_type)
        if date_from:
            filters.append(KnowledgeItem.created_at >= date_from)
        if date_to:
            filters.append(KnowledgeItem.created_at <= date_to)

        for f in filters:
            stmt = stmt.where(f)
            count_stmt = count_stmt.where(f)

        if sort == "oldest":
            stmt = stmt.order_by(asc(KnowledgeItem.created_at))
        elif sort == "updated":
            stmt = stmt.order_by(desc(KnowledgeItem.updated_at))
        else:
            stmt = stmt.order_by(desc(KnowledgeItem.created_at))

        total = self.session.execute(count_stmt).scalar() or 0
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)
        items = list(self.session.execute(stmt).scalars().all())

        return ItemListResult(items=items, total=total)

    def get_dashboard_data(self) -> dict:
        total_count = self.session.execute(
            select(func.count(KnowledgeItem.id))
        ).scalar() or 0

        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        recent_count = self.session.execute(
            select(func.count(KnowledgeItem.id)).where(
                KnowledgeItem.created_at >= seven_days_ago
            )
        ).scalar() or 0

        latest_items = list(
            self.session.execute(
                select(KnowledgeItem)
                .order_by(desc(KnowledgeItem.created_at))
                .limit(5)
            ).scalars().all()
        )

        category_distribution = list(
            self.session.execute(
                select(
                    func.coalesce(KnowledgeItem.category, "未分類"),
                    func.count(KnowledgeItem.id),
                )
                .group_by(KnowledgeItem.category)
                .order_by(func.count(KnowledgeItem.id).desc())
            ).all()
        )

        platform_distribution = list(
            self.session.execute(
                select(
                    KnowledgeItem.source_platform,
                    func.count(KnowledgeItem.id),
                )
                .group_by(KnowledgeItem.source_platform)
                .order_by(func.count(KnowledgeItem.id).desc())
            ).all()
        )

        content_type_distribution = list(
            self.session.execute(
                select(
                    func.coalesce(KnowledgeItem.content_type, "unknown"),
                    func.count(KnowledgeItem.id),
                )
                .group_by(KnowledgeItem.content_type)
                .order_by(func.count(KnowledgeItem.id).desc())
            ).all()
        )

        return {
            "total_count": total_count,
            "recent_count": recent_count,
            "latest_items": latest_items,
            "category_distribution": [
                {"label": label, "count": count}
                for label, count in category_distribution
            ],
            "platform_distribution": [
                {"label": label, "count": count}
                for label, count in platform_distribution
            ],
            "content_type_distribution": [
                {"label": label, "count": count}
                for label, count in content_type_distribution
            ],
        }

    def get_all_categories(self) -> list[str]:
        result = self.session.execute(
            select(KnowledgeItem.category)
            .where(KnowledgeItem.category.isnot(None))
            .distinct()
            .order_by(KnowledgeItem.category)
        ).scalars().all()
        return list(result)

    def rebuild_search_document(self, item: KnowledgeItem) -> None:
        keywords_text = " ".join(item.keywords or [])
        parts = [
            item.title or "",
            item.short_summary or "",
            item.full_summary or "",
            item.raw_content or "",
            keywords_text,
            item.category or "",
            item.author or "",
        ]
        item.search_document = "\n".join(part for part in parts if part).strip() or None

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, item: KnowledgeItem) -> None:
        self.session.refresh(item)
