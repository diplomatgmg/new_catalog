from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView

from apps.comparison.models import CPUComparison, GPUComparison
from apps.product.models import CPUModel


class IndexCompare(TemplateView):
    template_name = 'comparison/index.html'


class BaseComparison(ListView):
    context_object_name = 'comparison_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).first().products.select_related('brand')


class CPUComparisonListView(BaseComparison):
    template_name = 'comparison/includes/cpu.html'
    model = CPUComparison


class GPUComparisonListView(BaseComparison):
    template_name = 'comparison/includes/gpu.html'
    model = GPUComparison


PRODUCT_MODELS = settings.PRODUCT_MODELS

product_models = [apps.get_model(model_name) for model_name in PRODUCT_MODELS]


def comparison_add(request, slug):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

    user = request.user
    for model in product_models:
        product = model.objects.filter(slug=slug)
        if product.exists():
            product = product.last()
            comparison_model = model.get_comparison_model()
            comparison, created = comparison_model.objects.get_or_create(user=user)
            comparison.products.add(product)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def comparison_remove(request, slug):
    user = request.user
    for model in product_models:
        product = model.objects.filter(slug=slug)
        if product.exists():
            product = product.last()
            comparison_model = model.get_comparison_model()
            comparison, created = comparison_model.objects.get_or_create(user=user)
            comparison.products.remove(product)
    return redirect(request.META['HTTP_REFERER'])
