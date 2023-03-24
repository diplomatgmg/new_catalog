from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from apps.comparison.comparison import Comparison
from apps.comparison.models import CPUComparison, GPUComparison


class IndexCompare(TemplateView):
    template_name = "comparison/index.html"


class BaseComparison(ListView):
    template_name = "comparison/product-list.html"
    context_object_name = "comparison_list"
    comparison_fields = ()
    temp_user = None
    user_comparison_list = None

    def get_queryset(self, **kwargs):
        user_id = (
            self.request.user.id if self.request.user.is_authenticated else None
        )
        comparison_model = self.model.get_or_create(
            user_id, self.request.session
        )
        queryset = comparison_model.products.prefetch_related(
            "brand", "category"
        )
        return queryset.filter(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comparison_fields"] = self.comparison_fields
        return context


class CPUComparisonListView(BaseComparison):
    model = CPUComparison
    comparison_fields = (
        ("brand", "Бренд", ""),
        ("family", "Семейство", ""),
        ("model", "Модель", ""),
        ("num_cores", "Ядер", ""),
        ("base_clock", "Базовая частота", "МГц"),
    )


class GPUComparisonListView(BaseComparison):
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
