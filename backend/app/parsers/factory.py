from app.models.enums import SourcePlatform
from app.parsers.base import BaseParser
from app.parsers.generic import GenericWebParser
from app.parsers.social import FacebookParser, ThreadsParser
from app.parsers.youtube import YouTubeParser


class ParserFactory:
    def __init__(self, timeout_seconds: int = 20) -> None:
        self.timeout_seconds = timeout_seconds

    def get_parser(self, source_platform: SourcePlatform) -> BaseParser:
        if source_platform == SourcePlatform.YOUTUBE:
            return YouTubeParser(self.timeout_seconds)
        if source_platform == SourcePlatform.FACEBOOK:
            return FacebookParser(self.timeout_seconds)
        if source_platform == SourcePlatform.THREADS:
            return ThreadsParser(self.timeout_seconds)
        return GenericWebParser(self.timeout_seconds)
