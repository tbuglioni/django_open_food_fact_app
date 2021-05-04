from django.urls import path
from .views import substitute_views, my_food_view

app_name = "substitute"  # pour appeler la page en front

urlpatterns = [
    path("", substitute_views, name="substitute"),
    path("my_food", my_food_view, name="my_food"),
]