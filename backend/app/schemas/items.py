from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class IngestItemRequest(BaseModel):
    """Request body for the external ingestion API endpoint."""
    source_url: str
    source_platform: str = "generic_web"
    author: str | None = None
    published_at: datetime | None = None
    title: str | None = None
    short_summary: str | None = None
    full_summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    category: str | None = None
    content_type: str = "unknown"
    raw_content: str | None = None


class ItemFilterParams(BaseModel):
    q: str | None = None
    platform: str | None = None
    category: str | None = None
    content_type: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort: Literal["newest", "oldest", "updated"] = "newest"


class KnowledgeItemBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_url: str
    source_platform: str
    title: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    short_summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    category: str | None = None
    content_type: str | None = None
    processing_status: str
    updated_at: datetime
    created_at: datetime


class KnowledgeItemDetailResponse(KnowledgeItemBaseResponse):
    raw_content: str | None = None
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
    category_distribution: list[DashboardBucket]
    platform_distribution: list[DashboardBucket]
    content_type_distribution: list[DashboardBucket]


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
