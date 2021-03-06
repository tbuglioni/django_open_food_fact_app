from django.urls import path
from .views import (
    substitute_views,
    my_food_view,
    add_fav_view,
    rmv_fav_view,
    check_query_views,
)

app_name = "substitute"  # pour appeler la page en front

urlpatterns = [
    path("sub/<str:query>/", substitute_views, name="substitute"),
    path("my_food", my_food_view, name="my_food"),
    path("check_query", check_query_views, name="check_query"),
    path("add_fav", add_fav_view, name="add_fav"),
    path("rmv_fav", rmv_fav_view, name="rmv_fav"),
]
