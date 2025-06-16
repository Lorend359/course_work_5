from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор привычки с полной валидацией.
    """

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        is_pleasant = data.get("is_pleasant", False)
        reward = data.get("reward")
        linked_habit = data.get("linked_habit")
        duration = data.get("duration")
        periodicity = data.get("periodicity", 1)

        if is_pleasant:
            if reward or linked_habit:
                raise serializers.ValidationError(
                    "Приятная привычка не может иметь ни награды, ни связанную привычку."
                )
        else:
            if reward and linked_habit:
                raise serializers.ValidationError("Можно указать либо награду, либо связанную привычку, но не оба.")
            if not reward and not linked_habit:
                raise serializers.ValidationError(
                    "Укажите либо награду, либо связанную привычку для полезной привычки."
                )

        if linked_habit and not linked_habit.is_pleasant:
            raise serializers.ValidationError("Связанной может быть только приятная привычка.")

        if duration and duration > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")

        if periodicity and periodicity > 7:
            raise serializers.ValidationError("Периодичность не может быть реже 1 раза в 7 дней.")

        return data
