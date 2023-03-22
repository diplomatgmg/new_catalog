from django.urls import path

from apps.index.views import IndexTemplateView

app_name = "index"

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
]
