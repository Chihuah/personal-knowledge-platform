from urllib.parse import parse_qs, urlparse

from app.models.enums import ContentType, SourcePlatform
from app.parsers.base import ParsedContent
from app.parsers.generic import GenericWebParser


class YouTubeParser(GenericWebParser):
    def parse(self, url: str) -> ParsedContent:
        parsed = super().parse(url)
        video_id = _extract_video_id(url)
        if video_id and not parsed.thumbnail_url:
            parsed.thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        parsed.source_platform = SourcePlatform.YOUTUBE
        parsed.content_type = ContentType.VIDEO
        return parsed


def _extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path.strip("/") or None
    if parsed.hostname and parsed.hostname.endswith("youtube.com"):
        query = parse_qs(parsed.query)
        return query.get("v", [None])[0]
    return None
