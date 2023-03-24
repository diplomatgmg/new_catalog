from django.urls import path

from apps.comparison.views import (
    comparison_add,
    comparison_remove,
    CPUComparisonListView,
    GPUComparisonListView,
    IndexCompare,
)

app_name = "comparison"

urlpatterns = [
    path("", IndexCompare.as_view(), name="index"),
    path(
        "add/<slug:category_slug>/<slug:product_slug>",
        comparison_add,
        name="add",
    ),
    path(
        "remove/<slug:category_slug>/<slug:product_slug>",
        comparison_remove,
        name="remove",
    ),
    path("cpu/", CPUComparisonListView.as_view(), name="cpu"),
    path("gpu/", GPUComparisonListView.as_view(), name="gpu"),
]
