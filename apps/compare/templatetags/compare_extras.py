# comparison_tags.py
from django import template
from django.db.models import Prefetch

from apps.compare.models import CPUComparison, GPUComparison

register = template.Library()

COMPARE_MODELS = (
    CPUComparison,
    GPUComparison
)


@register.filter
def get_comparison_categories(user) -> list:
    comparison_list = (model.objects.filter(user=user).last() for model in COMPARE_MODELS)
    return [(model, model.products.select_related('category').first()) for model in comparison_list if model]
