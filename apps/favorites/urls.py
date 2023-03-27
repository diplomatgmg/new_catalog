from django.urls import path

from apps.favorites.views import FavoritesListView, favorites_add, favorites_remove

app_name = "favorites"

urlpatterns = [
    path("", FavoritesListView.as_view(), name="index"),
    path(
        "add/<slug:category_slug>/<slug:product_slug>",
        favorites_add,
        name="add",
    ),
    path(
        "remove/<slug:category_slug>/<slug:product_slug>",
        favorites_remove,
        name="remove",
    ),
]
