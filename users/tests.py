from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser


class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "302010Pass"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_user(self):
        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "NewPass123!"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_get_profile(self):
        token_url = reverse("users:token_obtain_pair")
        response = self.client.post(token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_profile(self):
        token_url = reverse("users:token_obtain_pair")
        response = self.client.post(token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        url = reverse("users:profile")
        response = self.client.patch(url, {"is_active": False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertFalse(updated_user.is_active)


