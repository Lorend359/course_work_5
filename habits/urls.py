from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HabitListCreateView, HabitRetrieveUpdateDestroyView, HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("", HabitListCreateView.as_view(), name="habit-list-create"),
    path("public/", PublicHabitListView.as_view(), name="public-habit-list"),
    path("<int:pk>/", HabitRetrieveUpdateDestroyView.as_view(), name="habit-detail"),
    path("", include(router.urls)),
]
