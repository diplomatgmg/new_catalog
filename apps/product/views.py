from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    model = CPUModel
    # Поля для фильтрации диапазона
    range_filter_fields = (
        'num_cores',
        'base_clock',
    )

    search_filter_fields = (
        'brand',
        'family',
        'model',
    )

    list_display_fields = (
        ('brand', 'Бренд', ''),
        ('family', 'Семейство', ''),
        ('num_cores', 'Количество ядер', 'ядер'),
        ('base_clock', 'Базовая частота', 'МГц'),
    )


class GPUListView(BaseProductListView):
    model = GPUModel
    range_filter_fields = (
        'base_clock',
        'boost_clock',
    )

    search_filter_fields = (
        'brand',
        'family',
        'model',
    )

    list_display_fields = (
        ('brand', 'Бренд', ''),
        ('family', 'Семейство', ''),
        ('model', 'Семейство', ''),
        ('base_clock', 'Базовая частота', 'МГц'),
        ('boost_clock', 'Базовая частота', 'МГц'),
    )
