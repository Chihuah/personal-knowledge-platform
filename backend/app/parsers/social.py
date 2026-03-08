from app.models.enums import ContentType, SourcePlatform
from app.parsers.base import ParsedContent
from app.parsers.generic import GenericWebParser


class FacebookParser(GenericWebParser):
    def parse(self, url: str) -> ParsedContent:
        parsed = super().parse(url)
        parsed.source_platform = SourcePlatform.FACEBOOK
        parsed.content_type = ContentType.POST
        return parsed


class ThreadsParser(GenericWebParser):
    def parse(self, url: str) -> ParsedContent:
        parsed = super().parse(url)
        parsed.source_platform = SourcePlatform.THREADS
        parsed.content_type = ContentType.POST
        return parsed
