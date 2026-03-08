from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field

from app.models.enums import ContentType, ProcessingStatus, SourcePlatform


class CreateItemRequest(BaseModel):
    url: AnyHttpUrl


class ItemFilterParams(BaseModel):
    q: str | None = None
    platform: SourcePlatform | None = None
    category: str | None = None
    status: ProcessingStatus | None = None
    content_type: ContentType | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort: Literal["newest", "oldest", "updated"] = "newest"


class KnowledgeItemBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_url: str
    source_platform: SourcePlatform
    title: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    captured_at: datetime
    thumbnail_url: str | None = None
    description: str | None = None
    short_summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    category: str | None = None
    content_type: ContentType | None = None
    processing_status: ProcessingStatus
    error_message: str | None = None
    updated_at: datetime


class KnowledgeItemDetailResponse(KnowledgeItemBaseResponse):
    raw_content: str | None = None
    cleaned_content: str | None = None
    full_summary: str | None = None


class PaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int


class KnowledgeItemListResponse(BaseModel):
    items: list[KnowledgeItemBaseResponse]
    pagination: PaginationResponse


class DashboardBucket(BaseModel):
    label: str
    count: int


class DashboardResponse(BaseModel):
    total_count: int
    recent_count: int
    latest_items: list[KnowledgeItemBaseResponse]
    failed_items: list[KnowledgeItemBaseResponse]
    category_distribution: list[DashboardBucket]
    status_distribution: list[DashboardBucket]
