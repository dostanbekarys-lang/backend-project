from celery import Celery
from app.core.config import settings
from app.services.email_service import send_email


celery_app = Celery(
    "leanstock_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to_email: str, subject: str, body: str):
    try:
        send_email(to_email, subject, body)
        return {
            "status": "sent",
            "to": to_email
        }
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)