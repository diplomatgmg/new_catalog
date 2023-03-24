from django.apps import apps
from django.conf import settings

PRODUCT_MODELS = settings.PRODUCT_MODELS

product_models = [apps.get_model(model_name) for model_name in PRODUCT_MODELS]


class Comparison:
    def __init__(self, request, category_slug):
        for model in product_models:
            products = model.objects.filter(category__slug=category_slug)
            if products.exists():
                self.product_models = model
                self.comparison_model = model.get_comparison_model()
                break

        if request.user.is_authenticated:
            self.comparison, _ = self.comparison_model.objects.get_or_create(
                user=request.user
            )
        else:
            session = request.session
            if not session.session_key:
                session.create()
            self.comparison, _ = self.comparison_model.objects.get_or_create(
                temp_user=session.session_key
            )

    def _get_product(self, product_slug):
        return self.product_models.objects.get(slug=product_slug)

    def update(self, product_slug, action="add"):
        product = self._get_product(product_slug)
        if action == "add":
            self.comparison.products.add(product)
        elif action == "remove":
            self.comparison.products.remove(product)
        else:
            raise ValueError("Invalid action: {}".format(action))
