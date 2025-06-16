from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import UserProfileSerializer, UserRegisterSerializer


@extend_schema(
    summary="Регистрация нового пользователя",
    description="Создаёт пользователя по e-mail и паролю. " "Возвращает данные зарегистрированного пользователя.",
    request=UserRegisterSerializer,
    responses={201: UserProfileSerializer},
)
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Просмотр и обновление профиля",
    description="Возвращает данные текущего пользователя (GET) и позволяет " "обновить их (PATCH).",
    responses=UserProfileSerializer,
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
