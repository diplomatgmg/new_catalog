from django.urls import include, path

from apps.product.find_model import find_model
from apps.product.views import CPUDetailView, CPUListView, GPUListView

app_name = "product"

urlpatterns = [
    path("", find_model, name="find-model"),
    path("cpu/", CPUListView.as_view(), name="cpu"),
    path("cpu/<slug:slug>/", CPUDetailView.as_view(), name="cpu-detail"),
    path("gpu/", GPUListView.as_view(), name="gpu"),
]
