from django.apps import apps
from django.conf import settings
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

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return (
                self.model.objects.filter(user=self.request.user)
                .first()
                .products.select_related("brand")
            )
        else:
            user_comparison_list = self.model.objects.filter(
                temp_user=self.request.session.session_key
            )
            if user_comparison_list.exists():
                return user_comparison_list.first().products.select_related(
                    "brand"
                )
            else:
                return []

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


PRODUCT_MODELS = settings.PRODUCT_MODELS

product_models = [apps.get_model(model_name) for model_name in PRODUCT_MODELS]


def comparison_add(request, slug):
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "error": "Invalid request method."}
        )

    for model in product_models:
        product = model.objects.filter(slug=slug)
        if product.exists():
            product = product.last()
            comparison_model = model.get_comparison_model()
            comparison = Comparison(request, comparison_model)
            comparison.add(product)

            return JsonResponse({"success": True})


def comparison_remove(request, slug):
    user = request.user
    for model in product_models:
        product = model.objects.filter(slug=slug)
        if product.exists():
            product = product.last()
            comparison_model = model.get_comparison_model()
            comparison, created = comparison_model.objects.get_or_create(
                user=user
            )
            comparison.products.remove(product)
    return redirect(request.META["HTTP_REFERER"])
