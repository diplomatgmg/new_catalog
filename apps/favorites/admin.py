from django.contrib import admin
from apps.favorites.models import FavoriteProducts


@admin.register(FavoriteProducts)
class FavoriteProductsAdmin(admin.ModelAdmin):
    pass
