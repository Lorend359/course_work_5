from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class HabitPagination(PageNumberPagination):
    page_size = 5


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Список и создание привычек пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user) | Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Просмотр, обновление и удаление привычки.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PublicHabitListView(generics.ListAPIView):
    """
    Список публичных привычек.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = HabitPagination


class HabitViewSet(ModelViewSet):
    """
    Просмотр своих и публичных привычек. Управление — только своими.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)