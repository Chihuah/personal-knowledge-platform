from celery import Celery

from app.core.config import get_settings


settings = get_settings()

celery_app = Celery("personal_knowledge_platform")
celery_app.conf.broker_url = settings.redis_url
celery_app.conf.result_backend = settings.redis_url
celery_app.conf.task_always_eager = settings.celery_task_always_eager
celery_app.conf.task_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.result_serializer = "json"
celery_app.conf.timezone = "UTC"
celery_app.conf.enable_utc = True
celery_app.conf.imports = ("app.tasks.jobs",)
