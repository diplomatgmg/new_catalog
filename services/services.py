from django.apps import apps
from django.conf import settings


def find_review_model_by_slug(category_slug):
    review_models = [
        apps.get_model(model_name) for model_name in settings.REVIEW_MODELS
    ]

    for review_model in review_models:
        if review_model.get_category_slug() == category_slug:
            return review_model


def find_product_model_by_slug(category_slug):
    product_models = [
        apps.get_model(model_name) for model_name in settings.PRODUCT_MODELS
    ]

    for product_model in product_models:
        if product_model.get_category_slug() == category_slug:
            return product_model


def get_product_by_slug(product_model, product_slug):
    return product_model.objects.get(slug=product_slug)
