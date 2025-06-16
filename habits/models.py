from django.conf import settings
from django.db import models


class Habit(models.Model):
    """
    Модель привычки.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        related_name="linked_to",
        verbose_name="Связанная привычка",
    )
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name="Вознаграждение")
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")
    duration = models.PositiveSmallIntegerField(verbose_name="Время на выполнение (сек)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    def __str__(self):
        return f"{self.action} в {self.place} в {self.time}"
