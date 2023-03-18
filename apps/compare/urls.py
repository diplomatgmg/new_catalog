from django.urls import path

from apps.compare.views import IndexCompare

app_name = 'compare'

urlpatterns = [
    path('', IndexCompare.as_view(), name='index'),



]
