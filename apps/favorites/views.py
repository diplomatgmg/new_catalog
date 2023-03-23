from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from apps.favorites.models import FavoriteProducts


class FavoritesListView(ListView):
    template_name = "favorites/favorites-list.html"
    model = FavoriteProducts
    context_object_name = "products"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_favorites = self.model.objects.filter(user=user).last()
            return user_favorites.get_favorites() if user_favorites else []
        else:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object_list
        return context
