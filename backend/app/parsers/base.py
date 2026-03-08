from datetime import datetime

from pydantic import BaseModel

from app.models.enums import ContentType, SourcePlatform


class ParsedContent(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    thumbnail_url: str | None = None
    raw_content: str | None = None
    cleaned_content: str | None = None
    source_platform: SourcePlatform
    content_type: ContentType = ContentType.UNKNOWN


class BaseParser:
    def parse(self, url: str) -> ParsedContent:
        raise NotImplementedError
