from fastapi import APIRouter, Depends

from app.api.responses import SuccessResponse, success_response
from app.dependencies import get_item_service
from app.schemas.items import DashboardResponse, KnowledgeItemBaseResponse
from app.services.item_service import ItemService


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(
    item_service: ItemService = Depends(get_item_service),
) -> SuccessResponse[DashboardResponse]:
    data = item_service.get_dashboard()
    return success_response(
        DashboardResponse(
            total_count=data["total_count"],
            recent_count=data["recent_count"],
            latest_items=[
                KnowledgeItemBaseResponse.model_validate(item)
                for item in data["latest_items"]
            ],
            failed_items=[
                KnowledgeItemBaseResponse.model_validate(item)
                for item in data["failed_items"]
            ],
            category_distribution=data["category_distribution"],
            status_distribution=data["status_distribution"],
        )
    )
