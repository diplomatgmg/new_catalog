from django.views.generic import ListView
from apps.product.models import Brand
from django.db.models import Min, Max


class BaseProductListView(ListView):
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    range_filter_fields = {}
    search_filter_fields = ()

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = self.model.objects.all().select_related('brand')

        if query:
            query = '.*' + ' '.join(query.lower().strip().split()) + '.*'
            query_new = query.replace(' ', '.')
            queryset_new = queryset.filter(slug__iregex=query_new)
            if not queryset_new:
                query_new = query.replace(' ', '.+')
                queryset = queryset.filter(slug__iregex=query_new)
            else:
                queryset = queryset_new

        brand = self.request.GET.getlist('brand')
        if brand:
            queryset = queryset.filter(brand__name__in=brand)

        for field_name in self.range_filter_fields:
            filter_value_min = self.request.GET.get(f'min_{field_name}')
            filter_value_max = self.request.GET.get(f'max_{field_name}')
            filter_kwargs = {}
            if filter_value_min:
                filter_kwargs[f'{field_name}__gte'] = filter_value_min
            if filter_value_max:
                filter_kwargs[f'{field_name}__lte'] = filter_value_max
            if filter_kwargs:
                queryset = queryset.filter(**filter_kwargs)

        for field in self.search_filter_fields:
            value = self.request.GET.getlist(field)
            if value:
                queryset = queryset.filter(**{f'{field}__in': value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['disabled_brands'] = []
        context['brands'] = []

        all_brands = set(self.model.objects.values_list('brand__name', flat=True))
        for brand in all_brands:
            if brand in set(product.brand.name for product in self.object_list):
                context['brands'].append(brand)
            else:
                context['disabled_brands'].append(brand)

        # context['brands'] = list(Brand.objects.filter(id__in=model_brands).order_by('name').values_list('name', flat=True))
        #
        # Для обработки поиска js
        context['search_fields'] = self.search_filter_fields

        if self.object_list.exists():
            for field_name in self.search_filter_fields:
                context[f'{field_name}_search_list'] = sorted(
                    set(getattr(product, field_name) for product in self.object_list))

            for field_name in self.range_filter_fields:
                context[f'{field_name}_min'] = min(getattr(product, field_name) for product in self.object_list)
                context[f'{field_name}_max'] = max(getattr(product, field_name) for product in self.object_list)

        #
        # for field in self.range_filter_fields:
        #     context[field] = self.queryset.values_list(field, flat=True)

        return context
