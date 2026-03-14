from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.responses import SuccessResponse, success_response
from app.dependencies import get_item_service, verify_api_key
from app.repositories.item_repository import ItemNotFoundError
from app.schemas.items import (
    IngestItemRequest,
    ItemFilterParams,
    KnowledgeItemBaseResponse,
    KnowledgeItemDetailResponse,
    KnowledgeItemListResponse,
    PaginationResponse,
)
from app.services.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest_item(
    payload: IngestItemRequest,
    _api_key: str = Depends(verify_api_key),
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[KnowledgeItemBaseResponse]:
    """External ingestion endpoint. Requires API Key in X-API-Key header."""
    item, created = item_service.ingest_item(payload)
    return success_response(KnowledgeItemBaseResponse.model_validate(item))


@router.get("")
def list_items(
    q: str | None = Query(default=None),
    platform: str | None = Query(default=None),
    category: str | None = Query(default=None),
    content_type: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    sort: str = Query(default="newest"),
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[KnowledgeItemListResponse]:
    filters = ItemFilterParams(
        q=q,
        platform=platform,
        category=category,
        content_type=content_type,
        date_from=item_service.parse_datetime(date_from),
        date_to=item_service.parse_datetime(date_to),
        page=page,
        page_size=page_size,
        sort=sort,
    )
    result = item_service.list_items(
        query=filters.q,
        platform=filters.platform,
        category=filters.category,
        content_type=filters.content_type,
        date_from=filters.date_from,
        date_to=filters.date_to,
        page=filters.page,
        page_size=filters.page_size,
        sort=filters.sort,
    )
    return success_response(
        KnowledgeItemListResponse(
            items=[
                KnowledgeItemBaseResponse.model_validate(item)
                for item in result.items
            ],
            pagination=PaginationResponse(
                total=result.total,
                page=filters.page,
                page_size=filters.page_size,
            ),
        )
    )


@router.get("/categories")
def list_categories(
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[list[str]]:
    return success_response(item_service.get_categories())


@router.get("/{item_id}")
def get_item(
    item_id: UUID,
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[KnowledgeItemDetailResponse]:
    try:
        item = item_service.get_item(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return success_response(KnowledgeItemDetailResponse.model_validate(item))
