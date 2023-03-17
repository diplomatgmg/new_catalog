from django.views.generic import ListView


class BaseProductListView(ListView):
    template_name = 'product/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        all_products = self.model.objects.all().select_related('brand')

        if query:
            query = '.*' + query.lower() + '.*'
            products = all_products.filter(slug__iregex=query.replace(' ', '.'))

            if not products:
                products = all_products.filter(slug__iregex=query.replace(' ', '.+'))

            if products:
                return products
            else:
                return all_products

        return all_products