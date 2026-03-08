import re

from bs4 import BeautifulSoup
import httpx
import trafilatura

from app.core.config import get_settings
from app.models.enums import ContentType, SourcePlatform
from app.parsers.base import BaseParser, ParsedContent


class GenericWebParser(BaseParser):
    def parse(self, url: str) -> ParsedContent:
        settings = get_settings()
        response = httpx.get(
            url,
            timeout=settings.parser_timeout_seconds,
            follow_redirects=True,
            headers={"User-Agent": "PersonalKnowledgePlatformBot/0.1"},
        )
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        extracted = trafilatura.extract(html, include_links=False, include_images=False)

        title = _read_meta(soup, "og:title") or (
            soup.title.string.strip() if soup.title and soup.title.string else None
        )
        description = _read_meta(soup, "description") or _read_meta(
            soup, "og:description"
        )
        thumbnail_url = _read_meta(soup, "og:image")
        author = _read_meta(soup, "author")

        return ParsedContent(
            source_platform=SourcePlatform.GENERIC_WEB,
            content_type=_infer_content_type(url, title or "", extracted or ""),
            title=title,
            author=author,
            thumbnail_url=thumbnail_url,
            description=description,
            cleaned_content=_normalize_text(extracted or description or title or ""),
        )


def _read_meta(soup: BeautifulSoup, key: str) -> str | None:
    meta = soup.find("meta", attrs={"property": key}) or soup.find(
        "meta", attrs={"name": key}
    )
    if not meta:
        return None
    content = meta.get("content")
    return content.strip() if isinstance(content, str) and content.strip() else None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _infer_content_type(url: str, title: str, content: str) -> ContentType:
    lowered = f"{url} {title} {content}".lower()
    if "tutorial" in lowered or "guide" in lowered:
        return ContentType.TUTORIAL
    if "tool" in lowered or "software" in lowered:
        return ContentType.TOOL
    return ContentType.ARTICLE
