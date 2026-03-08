from uuid import UUID

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.parsers.factory import ParserFactory
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.enrichment_service import EnrichmentService
from app.services.pipeline_service import PipelineService
from app.tasks.celery_app import celery_app


def _build_pipeline_service() -> PipelineService:
    settings = get_settings()
    session = SessionLocal()
    return PipelineService(
        repository=KnowledgeItemRepository(session),
        parser_factory=ParserFactory(settings.parser_timeout_seconds),
        enrichment_service=EnrichmentService(settings),
    )


@celery_app.task(name="app.tasks.jobs.process_item")
def process_item_task(item_id: str) -> None:
    pipeline = _build_pipeline_service()
    try:
        pipeline.process_item(UUID(item_id))
    finally:
        pipeline.repository.session.close()
