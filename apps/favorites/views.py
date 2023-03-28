from django.http import JsonResponse
from django.shortcuts import redirect

from apps.favorites.favorites import Favorites
from apps.favorites.models import Favorites as FavoritesModel
from mixins.ListViewMixin import ListViewMixin
from mixins.TemplateViewMixin import TemplateViewMixin


class FavoritesListView(ListViewMixin, TemplateViewMixin):
    template_name = "favorites/favorites-list.html"
    model = FavoritesModel
    context_object_name = "favorites"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_favorites = self.model.objects.filter(
                user=self.request.user
            ).last()
        else:
            user_favorites = self.model.objects.filter(
                temp_user=self.request.session.session_key
            ).last()
        return user_favorites.get_favorites() if user_favorites else []


def favorites_add(request, category_slug, product_slug):
    favorites = Favorites(request, category_slug)
    favorites.update(product_slug)
    return JsonResponse({"success": True})


def favorites_remove(request, category_slug, product_slug):
    favorites = Favorites(request, category_slug)
    favorites.update(product_slug, "remove")
    return redirect(request.META["HTTP_REFERER"])
