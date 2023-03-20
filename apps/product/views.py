from apps.product.base_views import BaseProductListView
from apps.product.models import Brand, CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_cores'] = sorted(self.queryset.values_list('num_cores', flat=True))
        context['clock_speed'] = sorted(self.queryset.values_list('clock_speed', flat=True))
        return context

    # Поля для фильтрации диапазона
    range_filter_fields = {
        "num_cores": "num_cores",
        "clock_speed": "clock_speed",
    }


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
    range_filter_fields = {}
