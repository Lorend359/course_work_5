from celery import shared_task
from notifications.tasks import send_telegram_message

@shared_task
def send_reminders():
    from .models import Habit
    from django.utils.timezone import now

    today = now().date()
    habits = Habit.objects.filter(periodicity=1, is_pleasant=False)

    for habit in habits:
        base_text = f"⏰ Напоминание: {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}."

        if habit.reward:
            base_text += f"\nНаграда: {habit.reward}."
        elif habit.linked_habit:
            base_text += f"\nВместо этого выполните приятную привычку: {habit.linked_habit.action}."
        else:
            base_text += "\n(❗️Нет награды или связанной привычки — проверьте корректность данных.)"

        send_telegram_message(base_text)

    return "Reminders sent"