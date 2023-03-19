from django.urls import path

from apps.comparison.views import cpu_comparison_add, IndexCompare, CPUComparisonListView, GPUComparisonListView

app_name = 'comparison'

urlpatterns = [
    path('', IndexCompare.as_view(), name='index'),

    path('cpu/', CPUComparisonListView.as_view(), name='cpu'),

    path('add/<slug:slug>', cpu_comparison_add, name='cpu_comparison_add'),

    path('gpu/', GPUComparisonListView.as_view(), name='gpu'),



]
