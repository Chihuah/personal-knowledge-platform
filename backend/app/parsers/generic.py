from bs4 import BeautifulSoup
import httpx
import trafilatura

from app.models.enums import ContentType, SourcePlatform
from app.parsers.base import BaseParser, ParsedContent


class GenericWebParser(BaseParser):
    def __init__(self, timeout_seconds: int = 20) -> None:
        self.timeout_seconds = timeout_seconds

    def parse(self, url: str) -> ParsedContent:
        response = httpx.get(
            url,
            timeout=self.timeout_seconds,
            follow_redirects=True,
            headers={"User-Agent": "PersonalKnowledgePlatform/0.1"},
        )
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else None
        description = _read_meta(
            soup,
            "description",
            "og:description",
            "twitter:description",
        )
        author = _read_meta(soup, "author", "article:author")
        thumbnail_url = _read_meta(soup, "og:image", "twitter:image")
        cleaned_content = trafilatura.extract(
            html,
            include_links=False,
            include_images=False,
            include_tables=False,
        )

        return ParsedContent(
            title=title,
            description=description,
            author=author,
            thumbnail_url=thumbnail_url,
            raw_content=html,
            cleaned_content=cleaned_content,
            source_platform=SourcePlatform.GENERIC_WEB,
            content_type=ContentType.ARTICLE,
        )


def _read_meta(soup: BeautifulSoup, *names: str) -> str | None:
    for name in names:
        tag = soup.find("meta", attrs={"name": name}) or soup.find(
            "meta", attrs={"property": name}
        )
        if tag and tag.get("content"):
            return str(tag["content"]).strip()
    return None
