from app.models.enums import ProcessingStatus, SourcePlatform
from app.models.knowledge_item import KnowledgeItem
from app.parsers.base import ParsedContent
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.enrichment_service import EnrichmentResult
from app.tasks.jobs import process_item_task


def test_process_item_task_updates_item_to_ready(
    db_session,
    testing_session_factory,
    monkeypatch,
) -> None:
    item = KnowledgeItem(
        source_url="https://example.com/ai-agent-guide",
        source_platform=SourcePlatform.GENERIC_WEB.value,
        processing_status=ProcessingStatus.QUEUED.value,
    )
    repository = KnowledgeItemRepository(db_session)
    repository.add(item)
    repository.commit()
    repository.refresh(item)

    class StubParser:
        def parse(self, url: str) -> ParsedContent:
            return ParsedContent(
                source_platform=SourcePlatform.GENERIC_WEB,
                title="AI Agent Guide",
                description="Build reliable AI agents.",
                raw_content="<html></html>",
                cleaned_content="Build reliable AI agents with search and memory.",
            )

    class StubParserFactory:
        def __init__(self, timeout_seconds: int) -> None:
            self.timeout_seconds = timeout_seconds

        def get_parser(self, platform: SourcePlatform) -> StubParser:
            return StubParser()

    class StubEnrichmentService:
        def __init__(self, settings) -> None:
            self.settings = settings

        def enrich(self, **_: object) -> EnrichmentResult:
            return EnrichmentResult(
                short_summary="Summary",
                full_summary="Detailed summary",
                keywords=["AI", "agents"],
                category="AI 工具",
                content_type="tutorial",
            )

    monkeypatch.setattr("app.tasks.jobs.SessionLocal", testing_session_factory)
    monkeypatch.setattr("app.tasks.jobs.ParserFactory", StubParserFactory)
    monkeypatch.setattr("app.tasks.jobs.EnrichmentService", StubEnrichmentService)

    process_item_task(str(item.id))
    verification_session = testing_session_factory()
    refreshed = KnowledgeItemRepository(verification_session).get_by_id(item.id)
    verification_session.close()

    assert refreshed is not None
    assert refreshed.processing_status == ProcessingStatus.READY.value
    assert refreshed.title == "AI Agent Guide"
    assert refreshed.short_summary == "Summary"
    assert refreshed.category == "AI 工具"
