from django.urls import path

from apps.compare.views import IndexCompare, CPUComparisonListView, GPUComparisonListView

app_name = 'comparison'

urlpatterns = [
    path('', IndexCompare.as_view(), name='index'),

    path('cpu/', CPUComparisonListView.as_view(), name='cpu'),
    path('gpu/', GPUComparisonListView.as_view(), name='gpu'),



]
