from apps.product.base_views import BaseProductListView
from apps.product.models import CPUModel


class CPUListView(BaseProductListView):
    template_name = 'product/includes/cpu-list.html'
    model = CPUModel
