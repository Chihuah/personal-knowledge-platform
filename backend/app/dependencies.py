from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db_session
from app.repositories.item_repository import KnowledgeItemRepository
from app.services.item_service import ItemService

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_item_service(
    session: Session = Depends(get_db_session),
) -> ItemService:
    return ItemService(
        repository=KnowledgeItemRepository(session),
    )


def verify_api_key(
    api_key: str | None = Security(api_key_header),
    settings: Settings = Depends(get_settings),
) -> str:
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key.",
        )
    return api_key
