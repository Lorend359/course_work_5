from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import CustomUser

@shared_task
def deactivate_inactive_users():
    threshold_date = now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(
        is_active=True
    ).filter(
        last_login__lt=threshold_date
    ) | CustomUser.objects.filter(
        is_active=True, last_login__isnull=True
    )

    count = inactive_users.update(is_active=False)
    print(f"🔒 Деактивировано пользователей: {count}")
    return f"Deactivated {count} users"
