from django.urls import path
from .views import (
    home_view, calculation_view
)

app_name = "calcul_kcal"

urlpatterns = [
    path("home/", home_view, name="home"),
    path("calculation_view/", calculation_view, name="calculation_view"),
]
