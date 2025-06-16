from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserProfileSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Просмотр и редактирование профиля.
    """
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
