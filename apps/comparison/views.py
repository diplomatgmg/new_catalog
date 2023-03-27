from django.http import JsonResponse
from django.shortcuts import redirect

from apps.comparison.base_comparison import BaseComparisonListView
from apps.comparison.comparison import Comparison
from apps.comparison.models import CPUComparison, GPUComparison


class CPUComparisonListView(BaseComparisonListView):
    model = CPUComparison
    comparison_fields = (
        ("brand", "Бренд", ""),
        ("family", "Семейство", ""),
        ("segment", "Сегмент", ""),
        ("model", "Модель", ""),
        ("year", "Год", ""),
        ("cores", "Ядер", ""),
        ("threads", "Потоков", ""),
        ("base_clock", "Базовая частота", "МГц"),
        ("integrated_graphics", "Встроенная графика", ""),
    )


class GPUComparisonListView(BaseComparisonListView):
    model = GPUComparison
    comparison_fields = (
        ("brand", "Бренд", ""),
        ("family", "Семейство", ""),
        ("model", "Модель", ""),
        ("base_clock", "Базовая частота", "МГц"),
        ("boost_clock", "Базовая частота", "МГц"),
    )


def comparison_add(request, category_slug, product_slug):
    comparison = Comparison(request, category_slug)
    comparison.update(product_slug)
    return JsonResponse({"success": True})


def comparison_remove(request, category_slug, product_slug):
    comparison = Comparison(request, category_slug)
    comparison.update(product_slug, "remove")
    return redirect(request.META["HTTP_REFERER"])
