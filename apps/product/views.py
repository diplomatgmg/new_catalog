from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel
    # Поля для фильтрации диапазона
    range_filter_fields = (
        'num_cores',
        'base_clock',
    )

    search_filter_fields = [
        'brand',
        'family',
        'model',
    ]

    list_display_fields = (
        ('brand', 'Бренд', ''),
        ('family', 'Семейство', ''),
        ('num_cores', 'Количество ядер', 'ядер'),
        ('base_clock', 'Базовая частота', 'МГц'),
    )


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
    range_filter_fields = (
        'base_clock',
        'boost_clock',
    )
