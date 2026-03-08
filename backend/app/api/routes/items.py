from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.api.responses import SuccessResponse, success_response
from app.dependencies import get_item_service
from app.schemas.items import (
    CreateItemRequest,
    ItemFilterParams,
    KnowledgeItemBaseResponse,
    KnowledgeItemDetailResponse,
    KnowledgeItemListResponse,
    PaginationResponse,
)
from app.services.item_service import (
    CaptureDisposition,
    ItemNotFoundError,
    ItemService,
)


router = APIRouter(prefix="/api/items", tags=["items"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_item(
    payload: CreateItemRequest,
    response: Response,
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[KnowledgeItemBaseResponse]:
    item, _, disposition = item_service.create_item(str(payload.url))
    if disposition == CaptureDisposition.EXISTING:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_202_ACCEPTED

    return success_response(KnowledgeItemBaseResponse.model_validate(item))


@router.get("")
def list_items(
    q: str | None = Query(default=None),
    platform: str | None = Query(default=None),
    category: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
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
        status=status_filter,
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
        status=filters.status,
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
                KnowledgeItemBaseResponse.model_validate(item) for item in result.items
            ],
            pagination=PaginationResponse(
                total=result.total,
                page=filters.page,
                page_size=filters.page_size,
            ),
        )
    )


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


@router.post("/{item_id}/reprocess")
def reprocess_item(
    item_id: UUID,
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[KnowledgeItemBaseResponse]:
    try:
        item, _ = item_service.reprocess_item(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return success_response(KnowledgeItemBaseResponse.model_validate(item))
