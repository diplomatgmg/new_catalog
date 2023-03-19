from django import template
from django.apps import apps
from django.conf import settings

register = template.Library()


COMPARISON_MODELS = settings.COMPARISON_MODELS

comparison_models = [apps.get_model(model_name) for model_name in COMPARISON_MODELS]


@register.filter
def get_comparison_categories(user) -> list:
    comparison_list = (model.objects.filter(user=user).last() for model in comparison_models)
    return [(model, model.products.select_related('category').first()) for model in comparison_list if model]
