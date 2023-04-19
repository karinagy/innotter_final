from celery import shared_task
from core.services import SESManager


@shared_task()
def send_mail(data: list) -> dict:
    return SESManager.send_mail(data)