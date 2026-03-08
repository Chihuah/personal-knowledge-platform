from app.models.enums import ProcessingStatus, SourcePlatform
from app.models.knowledge_item import KnowledgeItem
from app.parsers.base import ParsedContent
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.enrichment_service import EnrichmentResult
from app.services.pipeline_service import PipelineService


class FakeParser:
    def parse(self, url: str) -> ParsedContent:
        return ParsedContent(
            title="Parsed title",
            description="Parsed description",
            raw_content="<html>content</html>",
            cleaned_content="Parsed clean content",
            source_platform=SourcePlatform.GENERIC_WEB,
        )


class FakeParserFactory:
    def get_parser(self, source_platform: SourcePlatform) -> FakeParser:
        return FakeParser()


class FakeEnrichmentService:
    def enrich(self, **_: object) -> EnrichmentResult:
        return EnrichmentResult(
            short_summary="Short summary",
            full_summary="Full summary",
            keywords=["knowledge", "ai"],
            category="知識管理",
            content_type="影片",
        )


def test_pipeline_service_transitions_item_to_ready(db_session) -> None:
    item = KnowledgeItem(
        source_url="https://example.com/article",
        source_platform=SourcePlatform.GENERIC_WEB.value,
        processing_status=ProcessingStatus.QUEUED.value,
    )
    db_session.add(item)
    db_session.commit()

    service = PipelineService(
        repository=KnowledgeItemRepository(db_session),
        parser_factory=FakeParserFactory(),
        enrichment_service=FakeEnrichmentService(),
    )
    service.process_item(item.id)
    db_session.refresh(item)

    assert item.processing_status == ProcessingStatus.READY.value
    assert item.title == "Parsed title"
    assert item.short_summary == "Short summary"
    assert item.category == "知識管理"
    assert item.content_type == "video"
    assert item.search_document
