from django.apps import apps
from django.conf import settings


class Comparison:
    def __init__(self, request, category_slug):
        self.product_models = self._get_product_models()
        self.category_slug = category_slug
        self.product_model = self._get_product_model()
        self.comparison_model = self.get_comparison_model()
        self.comparison = self._get_or_create_comparison(request)

    def get_comparison_model(self):
        return self.product_model.get_comparison_model()

    def _get_product_model(self):
        for model in self.product_models:
            product = model.objects.first()
            if product.category.slug == self.category_slug:
                return model

    @staticmethod
    def _get_product_models():
        return [
            apps.get_model(model_name) for model_name in settings.PRODUCT_MODELS
        ]

    def _get_or_create_comparison(self, request):
        comparison_model = self.comparison_model
        session_key = request.session.session_key

        if request.user.is_authenticated:
            comparison, _ = comparison_model.objects.get_or_create(
                user=request.user
            )
        elif session_key:
            comparison, _ = comparison_model.objects.get_or_create(
                temp_user=session_key
            )
        else:
            request.session.create()
            comparison, _ = comparison_model.objects.get_or_create(
                temp_user=request.session.session_key
            )

        return comparison

    def _get_product(self, product_slug):
        return self.product_model.objects.get(slug=product_slug)

    def update(self, product_slug, action="add"):
        product = self._get_product(product_slug)
        comparison = self.comparison.products

        if action == "add":
            comparison.add(product)
        elif action == "remove":
            comparison.remove(product)
        else:
            raise ValueError(f"Invalid action: {action}")
