from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel

    # Поля для фильтрации диапазона
    range_filter_fields = {
        "num_cores": "num_cores",
        "clock_speed": "clock_speed",
    }


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
    range_filter_fields = {}
