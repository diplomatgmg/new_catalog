from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel
    # Поля для фильтрации диапазона
    range_filter_fields = {
        'num_cores': 'num_cores',
        'base_clock': 'base_clock',
    }

    search_filter_fields = (
        'family',
        'model',
    )

    def get_queryset(self):
        queryset = super().get_queryset()



        return queryset


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
    range_filter_fields = {
        'base_clock': 'base_clock',
        'boost_clock': 'boost_clock',
    }
