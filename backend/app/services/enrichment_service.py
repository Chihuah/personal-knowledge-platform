import json
from textwrap import shorten

from openai import OpenAI
from pydantic import BaseModel, Field

from app.core.config import Settings
from app.models.enums import ContentType


class EnrichmentResult(BaseModel):
    short_summary: str
    full_summary: str
    keywords: list[str] = Field(default_factory=list)
    category: str
    content_type: str


class EnrichmentService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def enrich(
        self,
        *,
        title: str | None,
        source_platform: str,
        content_text: str | None,
        content_type: str | None,
    ) -> EnrichmentResult:
        if not content_text:
            content_text = title or "No content available."

        if self.client is None:
            return self._fallback(title, source_platform, content_text, content_type)

        prompt = (
            "You are enriching a private knowledge item. Return JSON only with keys "
            "short_summary, full_summary, keywords, category, content_type. Use Traditional Chinese."
        )
        content = (
            f"title: {title or ''}\n"
            f"platform: {source_platform}\n"
            f"content_type: {content_type or 'unknown'}\n"
            f"content:\n{content_text[:12000]}"
        )
        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": content},
                ],
            )
            output = getattr(response, "output_text", "") or ""
            return EnrichmentResult.model_validate(json.loads(output))
        except Exception:
            return self._fallback(title, source_platform, content_text, content_type)

    def _fallback(
        self,
        title: str | None,
        source_platform: str,
        content_text: str,
        content_type: str | None,
    ) -> EnrichmentResult:
        short_summary = shorten(content_text.replace("\n", " "), width=180, placeholder="...")
        full_summary = shorten(content_text.replace("\n", " "), width=420, placeholder="...")
        terms = [part.strip(" ,.;:!?") for part in (title or "").split() if part.strip()]
        keywords = list(dict.fromkeys((terms + [source_platform])[:5]))
        return EnrichmentResult(
            short_summary=short_summary or (title or "尚無摘要"),
            full_summary=full_summary or (title or "尚無摘要"),
            keywords=keywords,
            category="未分類",
            content_type=content_type or ContentType.UNKNOWN.value,
        )
