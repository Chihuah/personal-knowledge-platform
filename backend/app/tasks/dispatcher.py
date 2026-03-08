from dataclasses import dataclass
from uuid import UUID

from app.core.config import Settings
from app.services.pipeline_service import PipelineService
from app.tasks.jobs import process_item_task


@dataclass
class DispatchResult:
    attempted: bool
    message: str


class TaskDispatcher:
    def __init__(self, settings: Settings, pipeline_service: PipelineService) -> None:
        self.settings = settings
        self.pipeline_service = pipeline_service

    def enqueue_ingestion(self, item_id: UUID) -> DispatchResult:
        if self.settings.tasks_mode == "celery":
            process_item_task.delay(str(item_id))
            return DispatchResult(True, "Item queued via Celery.")

        self.pipeline_service.process_item(item_id)
        return DispatchResult(True, "Item processed inline.")
