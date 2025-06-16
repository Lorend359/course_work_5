from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer


class HabitPagination(PageNumberPagination):
    page_size = 5


@extend_schema(
    summary="Получить список привычек пользователя",
    description="Возвращает список всех привычек, созданных авторизованным пользователем.",
    responses=HabitSerializer,
)
class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Создать новую привычку",
        description="Позволяет авторизованному пользователю создать новую привычку.",
        request=HabitSerializer,
        responses={201: HabitSerializer},
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Получить, обновить или удалить привычку по ID",
    description="Позволяет просматривать, редактировать или удалять привычку."
                " Только владелец может изменять или удалять.",
    responses=HabitSerializer,
)
class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


@extend_schema(
    summary="Список публичных привычек",
    description="Отображает список привычек, помеченных как публичные.",
    responses=HabitSerializer,
)
class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination


@extend_schema(
    summary="Работа с привычками (ViewSet)",
    description="Возвращает привычки пользователя и публичные привычки. Используется для CRUD через ViewSet.",
)
class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
