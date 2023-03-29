from django.urls import path

from apps.review.views import ReviewListCreateView

app_name = "review"

urlpatterns = [
    path("", ReviewListCreateView.as_view(), name="list-create"),
]
