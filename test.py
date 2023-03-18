from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


def range_filter(queryset, name_field, min_value, max_value):
    min_field = {name_field + '__gte': min_value}
    max_field = {name_field + '__lte': max_value}
    if min_value:
        queryset = queryset.filter(**min_field)
    if max_value:
        queryset = queryset.filter(**max_field)
    return queryset


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по бренду
        brand = self.request.GET.getlist('brand')
        if brand:
            queryset = queryset.filter(brand__name__in=brand)

        # Фильтрация по количеству ядер
        min_num_cores = self.request.GET.get('min_num_cores')
        max_num_cores = self.request.GET.get('max_num_cores')
        queryset = range_filter(queryset, 'num_cores', min_num_cores, max_num_cores)

        # Фильтрация по частоте ядра
        min_clock_speed = self.request.GET.get('min_clock_speed')
        max_clock_speed = self.request.GET.get('max_clock_speed')
        queryset = range_filter(queryset, 'clock_speed', min_clock_speed, max_clock_speed)

        return queryset


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
