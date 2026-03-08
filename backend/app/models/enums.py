from enum import StrEnum


class SourcePlatform(StrEnum):
    FACEBOOK = "facebook"
    THREADS = "threads"
    YOUTUBE = "youtube"
    GENERIC_WEB = "generic_web"


class ProcessingStatus(StrEnum):
    RECEIVED = "received"
    QUEUED = "queued"
    PARSING = "parsing"
    PARSED = "parsed"
    ANALYZING = "analyzing"
    READY = "ready"
    FAILED = "failed"


class ContentType(StrEnum):
    ARTICLE = "article"
    POST = "post"
    VIDEO = "video"
    TOOL = "tool"
    TUTORIAL = "tutorial"
    RESOURCE = "resource"
    UNKNOWN = "unknown"
