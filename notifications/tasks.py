import httpx
from django.conf import settings

TELEGRAM_API = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_message(text: str):
    """Отправляет сообщение в Telegram"""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        return

    try:
        httpx.post(
            TELEGRAM_API,
            data={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": text,
            },
            timeout=10,
        )
    except Exception as e:
        print(f"❌ Ошибка при отправке в Telegram: {e}")
