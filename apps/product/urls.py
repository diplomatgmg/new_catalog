from django.urls import include, path

from apps.product.find_model import find_model
from apps.product.views import (
    CPUDetailView,
    CPUListView,
    GPUDetailView,
    GPUListView,
)

app_name = "product"

urlpatterns = [
    path("", find_model, name="find-model"),
    path(
        "<slug:category_slug>/<slug:product_slug>/reviews",
        include("apps.review.urls", "review"),
    ),
    path("cpu/", CPUListView.as_view(), name="cpu"),
    path("cpu/<slug:slug>/", CPUDetailView.as_view(), name="cpu-detail"),
    path("gpu/", GPUListView.as_view(), name="gpu"),
    path("gpu/<slug:slug>/", GPUDetailView.as_view(), name="gpu-detail"),
]
