from celery import Celery

app = Celery("f5mobile_cms", broker="redis://45.124.95.107:6379/0")

app.conf.update(
    result_backend="redis://45.124.95.107:6379/1",
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
