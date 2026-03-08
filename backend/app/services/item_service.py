from datetime import datetime
from urllib.parse import urlparse
from uuid import UUID

from app.models.enums import ProcessingStatus, SourcePlatform
from app.models.knowledge_item import KnowledgeItem
from app.repositories.item_repository import ItemListResult, KnowledgeItemRepository
from app.tasks.dispatcher import DispatchResult, TaskDispatcher


class ItemAlreadyExistsError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class ItemService:
    def __init__(
        self,
        repository: KnowledgeItemRepository,
        task_dispatcher: TaskDispatcher,
    ) -> None:
        self.repository = repository
        self.task_dispatcher = task_dispatcher

    def create_item(self, source_url: str) -> tuple[KnowledgeItem, DispatchResult]:
        if self.repository.get_by_url(source_url):
            raise ItemAlreadyExistsError("This URL has already been captured.")

        item = KnowledgeItem(
            source_url=source_url,
            source_platform=detect_source_platform(source_url).value,
            processing_status=ProcessingStatus.RECEIVED.value,
        )
        self.repository.add(item)
        self.repository.rebuild_search_document(item)
        self.repository.add_log(
            knowledge_item_id=item.id,
            action="item_created",
            status="success",
            message="Knowledge item created.",
        )
        self.repository.update_status(item, ProcessingStatus.QUEUED)
        dispatch_result = self.task_dispatcher.enqueue_ingestion(item.id)
        self.repository.add_log(
            knowledge_item_id=item.id,
            action="ingestion_enqueued",
            status="success" if dispatch_result.attempted else "skipped",
            message=dispatch_result.message,
        )
        self.repository.commit()
        self.repository.refresh(item)
        return item, dispatch_result

    def list_items(self, **filters: object) -> ItemListResult:
        return self.repository.list_items(**filters)

    def get_item(self, item_id: UUID) -> KnowledgeItem:
        item = self.repository.get_by_id(item_id)
        if item is None:
            raise ItemNotFoundError("Knowledge item not found.")
        return item

    def get_dashboard(self) -> dict[str, object]:
        return self.repository.get_dashboard()

    def reprocess_item(self, item_id: UUID) -> tuple[KnowledgeItem, DispatchResult]:
        item = self.get_item(item_id)
        item.error_message = None
        self.repository.update_status(item, ProcessingStatus.QUEUED)
        self.repository.add_log(
            knowledge_item_id=item.id,
            action="reprocess_requested",
            status="success",
            message="Item queued for reprocessing.",
        )
        dispatch_result = self.task_dispatcher.enqueue_ingestion(item.id)
        self.repository.add_log(
            knowledge_item_id=item.id,
            action="reprocess_enqueued",
            status="success" if dispatch_result.attempted else "skipped",
            message=dispatch_result.message,
        )
        self.repository.commit()
        self.repository.refresh(item)
        return item, dispatch_result

    def parse_datetime(self, value: str | None) -> datetime | None:
        if value is None:
            return None
        return datetime.fromisoformat(value)


def detect_source_platform(source_url: str) -> SourcePlatform:
    hostname = urlparse(source_url).hostname or ""

    if hostname.endswith("facebook.com") or hostname.endswith("fb.watch"):
        return SourcePlatform.FACEBOOK
    if hostname.endswith("threads.net"):
        return SourcePlatform.THREADS
    if hostname.endswith("youtube.com") or hostname.endswith("youtu.be"):
        return SourcePlatform.YOUTUBE
    return SourcePlatform.GENERIC_WEB
