from uuid import UUID

from app.models.enums import ProcessingStatus, SourcePlatform
from app.parsers.factory import ParserFactory
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.enrichment_service import EnrichmentService


class PipelineService:
    def __init__(
        self,
        *,
        repository: KnowledgeItemRepository,
        parser_factory: ParserFactory,
        enrichment_service: EnrichmentService,
    ) -> None:
        self.repository = repository
        self.parser_factory = parser_factory
        self.enrichment_service = enrichment_service

    def process_item(self, item_id: UUID) -> None:
        item = self.repository.get_by_id(item_id)
        if item is None:
            return

        try:
            self.repository.update_status(item, ProcessingStatus.PARSING)
            parser = self.parser_factory.get_parser(SourcePlatform(item.source_platform))
            parsed = parser.parse(item.source_url)
            item.source_platform = parsed.source_platform.value
            item.title = parsed.title
            item.description = parsed.description
            item.author = parsed.author
            item.published_at = parsed.published_at
            item.thumbnail_url = parsed.thumbnail_url
            item.raw_content = parsed.raw_content
            item.cleaned_content = parsed.cleaned_content
            item.content_type = parsed.content_type.value
            self.repository.rebuild_search_document(item)
            self.repository.add_log(
                knowledge_item_id=item.id,
                action="parsed",
                status="success",
                message="Content parsed successfully.",
            )
            self.repository.update_status(item, ProcessingStatus.PARSED)

            self.repository.update_status(item, ProcessingStatus.ANALYZING)
            enrichment = self.enrichment_service.enrich(
                title=item.title,
                source_platform=item.source_platform,
                content_text=item.cleaned_content or item.description,
                content_type=item.content_type,
            )
            item.short_summary = enrichment.short_summary
            item.full_summary = enrichment.full_summary
            item.keywords = enrichment.keywords
            item.category = enrichment.category
            item.content_type = enrichment.content_type
            self.repository.rebuild_search_document(item)
            self.repository.add_log(
                knowledge_item_id=item.id,
                action="enriched",
                status="success",
                message="AI enrichment completed.",
            )
            self.repository.update_status(item, ProcessingStatus.READY)
            self.repository.commit()
        except Exception as exc:
            item.processing_status = ProcessingStatus.FAILED.value
            item.error_message = str(exc)
            self.repository.add_log(
                knowledge_item_id=item.id,
                action="pipeline_failed",
                status="failed",
                message=str(exc),
            )
            self.repository.commit()
