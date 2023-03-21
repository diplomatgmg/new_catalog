from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel, GPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel
    # Поля для фильтрации диапазона
    range_filter_fields = {
        "num_cores": "num_cores",
        "base_clock": "base_clock",
    }

    def get_queryset(self):
        queryset = super().get_queryset()

        family = self.request.GET.getlist('family')
        if family:
            queryset = queryset.filter(family__in=family)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['family_list'] = set(self.queryset.values_list('family', flat=True))
        context['num_cores'] = set(self.queryset.values_list('num_cores', flat=True))
        context['base_clock'] = set(self.queryset.values_list('base_clock', flat=True))

        return context


class GPUListView(BaseProductListView):
    template_name = 'product/includes/gpu-list.html'
    model = GPUModel
    range_filter_fields = {
        "base_clock": "base_clock",
        "boost_clock": "boost_clock",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_clock'] = set(self.queryset.values_list('base_clock', flat=True))
        context['boost_clock'] = set(self.queryset.values_list('boost_clock', flat=True))
        return context
