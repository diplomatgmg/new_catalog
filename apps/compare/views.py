from django.views.generic import ListView, TemplateView

from apps.compare.models import CPUComparison, GPUComparison


class IndexCompare(TemplateView):
    template_name = 'comparison/index.html'


class BaseComparison(ListView):
    context_object_name = 'comparison_list'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).first().products.select_related('brand').all()




class CPUComparisonListView(BaseComparison):
    template_name = 'comparison/includes/cpu.html'
    model = CPUComparison


class GPUComparisonListView(BaseComparison):
    template_name = 'comparison/includes/gpu.html'
    model = GPUComparison
