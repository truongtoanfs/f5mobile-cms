from celery import Celery
from config import settings

app = Celery("f5mobile_cms", broker=settings.REDIS_BROKER_URL)

app.conf.update(
    broker_connection_retry_on_startup=True,
    result_backend=settings.REDIS_BACKEND_URL,
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
