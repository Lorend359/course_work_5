from rest_framework import serializers

from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "email", "is_active")
        read_only_fields = ("email",)
