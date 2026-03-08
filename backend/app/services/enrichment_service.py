import json
from textwrap import shorten

from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

from app.core.config import Settings
from app.models.enums import ContentType


class EnrichmentResult(BaseModel):
    short_summary: str
    full_summary: str
    keywords: list[str] = Field(default_factory=list)
    category: str
    content_type: str

    @field_validator("content_type", mode="before")
    @classmethod
    def normalize_content_type(cls, value: object) -> str:
        return normalize_content_type(value)


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
            content_type=normalize_content_type(content_type),
        )


def normalize_content_type(value: object) -> str:
    if not isinstance(value, str):
        return ContentType.UNKNOWN.value

    normalized = value.strip().lower()
    mapping = {
        "article": ContentType.ARTICLE.value,
        "文章": ContentType.ARTICLE.value,
        "post": ContentType.POST.value,
        "貼文": ContentType.POST.value,
        "video": ContentType.VIDEO.value,
        "影片": ContentType.VIDEO.value,
        "video clip": ContentType.VIDEO.value,
        "tool": ContentType.TOOL.value,
        "工具": ContentType.TOOL.value,
        "tutorial": ContentType.TUTORIAL.value,
        "教學": ContentType.TUTORIAL.value,
        "resource": ContentType.RESOURCE.value,
        "資源": ContentType.RESOURCE.value,
        "unknown": ContentType.UNKNOWN.value,
        "未知": ContentType.UNKNOWN.value,
    }
    return mapping.get(normalized, ContentType.UNKNOWN.value)
