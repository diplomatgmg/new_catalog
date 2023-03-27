from django.contrib import admin

from apps.favorites.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    raw_id_fields = ("cpu", "gpu")
