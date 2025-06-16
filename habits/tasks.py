from celery import shared_task
from notifications.tasks import send_telegram_message

@shared_task
def send_test_reminder():
    send_telegram_message("⏰ Привет из Celery + Telegram!")
    return "Done"
