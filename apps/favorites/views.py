from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.favorites.favorites import Favorites
from apps.favorites.models import Favorites as FavoritesModel


class FavoritesListView(TemplateView):
    template_name = "favorites/favorites-list.html"
    model = FavoritesModel
    object_list = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object_list
        return context


def favorites_add(request, category_slug, product_slug):
    favorites = Favorites(request, category_slug)
    favorites.update(product_slug)
    return JsonResponse({"success": True})


def favorites_remove(request, category_slug, product_slug):
    favorites = Favorites(request, category_slug)
    favorites.update(product_slug, "remove")
    return redirect(request.META["HTTP_REFERER"])
