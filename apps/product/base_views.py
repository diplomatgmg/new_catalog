from django.views.generic import ListView


class BaseProductListView(ListView):
    template_name = 'product/product-list.html'
    context_object_name = 'products'
