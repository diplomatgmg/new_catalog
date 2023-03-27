from django.apps import apps
from django.conf import settings

from apps.favorites.models import Favorites as FavoritesModel


class Favorites:
    def __init__(self, request, category_slug):
        self.product_models = self._get_product_models()
        self.category_slug = category_slug
        self.product_model = self._get_product_model()
        self.favorites_model = FavoritesModel
        self.favorites = self._get_or_create_favorites(request)

    @staticmethod
    def _get_product_models():
        return [
            apps.get_model(model_name) for model_name in settings.PRODUCT_MODELS
        ]

    def _get_product_model(self):
        for model in self.product_models:
            product = model.objects.first()
            if product.category.slug == self.category_slug:
                return model

    def _get_or_create_favorites(self, request):
        favorites_model = self.favorites_model
        session_key = request.session.session_key or request.session.create()

        if request.user.is_authenticated:
            favorites, _ = favorites_model.objects.get_or_create(
                user=request.user
            )
        else:
            favorites, _ = favorites_model.objects.get_or_create(
                temp_user=session_key
            )

        return favorites

    def _get_product(self, product_slug):
        return self.product_model.objects.get(slug=product_slug)

    def update(self, product_slug, action="add"):
        product = self._get_product(product_slug)
        favorites_category = getattr(self.favorites, self.category_slug)

        if action == "add":
            favorites_category.add(product)
        elif action == "remove":
            favorites_category.remove(product)
        else:
            raise ValueError(f"Invalid action: {action}")
