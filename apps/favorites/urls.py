from django.urls import path

from apps.favorites.views import FavoritesListView

app_name = "favorites"

urlpatterns = [
    path("", FavoritesListView.as_view(), name="index"),
]
