from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from habits.models import Habit
from users.models import CustomUser


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@example.com", password="302010Pass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "place": "дом",
            "time": "08:00:00",
            "action": "зарядка",
            "is_pleasant": False,
            "reward": "кофе",
            "linked_habit": None,
            "periodicity": 1,
            "duration": 20,
            "is_public": True,
        }

    def test_create_habit(self):
        url = reverse("habits-list")
        response = self.client.post(url, self.habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().action, "зарядка")

    def test_get_user_habits(self):
        Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits-detail", kwargs={"pk": habit.pk})

        response = self.client.patch(url, {"action": "йога", "reward": "кофе"}, format="json")

        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE DATA:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "йога")

    def test_delete_habit(self):
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        url = reverse("habits-detail", kwargs={"pk": habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
