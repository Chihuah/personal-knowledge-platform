from enum import StrEnum


class SourcePlatform(StrEnum):
    FACEBOOK = "facebook"
    THREADS = "threads"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    BLOG = "blog"
    PODCAST = "podcast"
    GENERIC_WEB = "generic_web"


class ProcessingStatus(StrEnum):
    READY = "ready"
    FAILED = "failed"


class ContentType(StrEnum):
    ARTICLE = "article"
    POST = "post"
    VIDEO = "video"
    TOOL = "tool"
    TUTORIAL = "tutorial"
    RESOURCE = "resource"
    NEWS = "news"
    UNKNOWN = "unknown"
