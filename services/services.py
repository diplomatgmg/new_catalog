from django.apps import apps
from django.conf import settings


def get_all_slug_models():
    return [slug for slug in settings.MODEL_SLUG_PREFIXES]


def get_product_models():
    product_models = [
        apps.get_model(model_name) for model_name in settings.PRODUCT_MODELS
    ]
    return product_models


def get_comparison_models():
    comparison_models = [
        apps.get_model(model_name) for model_name in settings.COMPARISON_MODELS
    ]
    return comparison_models


def get_review_models():
    review_models = [
        apps.get_model(model_name) for model_name in settings.REVIEW_MODELS
    ]
    return review_models


def find_review_model_by_slug(category_slug):
    review_models = get_review_models()

    for review_model in review_models:
        if review_model.get_category_slug() == category_slug:
            return review_model


def find_product_model_by_slug(category_slug):
    product_models = get_product_models()

    for product_model in product_models:
        if product_model.get_category_slug() == category_slug:
            return product_model


def get_product_by_slug(product_model, product_slug):
    return product_model.objects.get(slug=product_slug)
