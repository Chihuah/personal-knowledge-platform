from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db_session
from app.parsers.factory import ParserFactory
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.enrichment_service import EnrichmentService
from app.services.item_service import ItemService
from app.services.pipeline_service import PipelineService
from app.tasks.dispatcher import TaskDispatcher


def get_parser_factory(
    settings: Settings = Depends(get_settings),
) -> ParserFactory:
    return ParserFactory(settings.parser_timeout_seconds)


def get_enrichment_service(
    settings: Settings = Depends(get_settings),
) -> EnrichmentService:
    return EnrichmentService(settings)


def get_pipeline_service(
    session: Session = Depends(get_db_session),
    parser_factory: ParserFactory = Depends(get_parser_factory),
    enrichment_service: EnrichmentService = Depends(get_enrichment_service),
) -> PipelineService:
    return PipelineService(
        repository=KnowledgeItemRepository(session),
        parser_factory=parser_factory,
        enrichment_service=enrichment_service,
    )


def get_task_dispatcher(
    settings: Settings = Depends(get_settings),
    pipeline_service: PipelineService = Depends(get_pipeline_service),
) -> TaskDispatcher:
    return TaskDispatcher(settings=settings, pipeline_service=pipeline_service)


def get_item_service(
    session: Session = Depends(get_db_session),
    task_dispatcher: TaskDispatcher = Depends(get_task_dispatcher),
) -> ItemService:
    return ItemService(
        repository=KnowledgeItemRepository(session),
        task_dispatcher=task_dispatcher,
    )
