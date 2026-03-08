from fastapi import FastAPI

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.items import router as items_router
from app.api.exception_handlers import register_exception_handlers
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
app.include_router(health_router)
app.include_router(items_router)
app.include_router(dashboard_router)
register_exception_handlers(app)
