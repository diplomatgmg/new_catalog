from django.urls import path

from apps.review.views import CPUReviewCreateView

app_name = "review"

urlpatterns = [
    path("cpu/<slug:slug>/", CPUReviewCreateView.as_view(), name="create"),
]
