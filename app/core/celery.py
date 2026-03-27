from celery import Celery
from app.core.config import settings

celery_app=Celery(
    "insureflow",
    broker=settings.REDDIS_URL,
    backend=settings.REDDIS_URL,
    include=["app.tasks.claim_tasks"]

)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

)

