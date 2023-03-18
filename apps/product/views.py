from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по бренду
        brand = self.request.GET.getlist('brand')
        if brand:
            queryset = queryset.filter(brand__name__in=brandux)



        # Фильтрация по количеству ядер
        num_cores = self.request.GET.getlist('num_cores')
        if num_cores:
            queryset = queryset.filter(num_cores__in=num_cores)

        # Фильтрация по частоте ядра
        min_clock_speed = self.request.GET.get('min_clock_speed')
        max_clock_speed = self.request.GET.get('max_clock_speed')
        if min_clock_speed or max_clock_speed:
            if min_clock_speed:
                queryset = queryset.filter(clock_speed__gte=min_clock_speed)
            if max_clock_speed:
                queryset = queryset.filter(clock_speed__lte=max_clock_speed)

        return queryset


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
