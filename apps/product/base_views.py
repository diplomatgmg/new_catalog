from django.views.generic import ListView


class BaseProductListView(ListView):
    template_name = 'product/product-list.html'
    context_object_name = 'products'
    range_filter_fields = None

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = self.model.objects.all().select_related('brand')

        # Фильтруем queryset строго
        if query:
            # Очищаем запрос от лишних пробелов
            query = '.*' + ' '.join(query.lower().strip().split()) + '.*'
            query_new = query.replace(' ', '.')
            queryset_new = queryset.filter(slug__iregex=query_new)

            # Если ничего не находим, фильтруем не строго
            if not queryset_new:
                query_new = query.replace(' ', '.+')
                queryset = queryset.filter(slug__iregex=query_new)
            else:
                queryset = queryset_new

        # Фильтрация бренда
        brand = self.request.GET.getlist('brand')
        if brand:
            queryset = queryset.filter(brand__name__in=brand)

        # Фильтрация диапазона значений
        for field_name, filter_name in self.range_filter_fields.items():
            filter_value_min = self.request.GET.get(f"min_{filter_name}")
            filter_value_max = self.request.GET.get(f"max_{filter_name}")
            if filter_value_min and filter_value_max:
                queryset = queryset.filter(**{
                    f"{field_name}__range": (filter_value_min, filter_value_max),
                })
            elif filter_value_min:
                queryset = queryset.filter(**{
                    f"{field_name}__gte": filter_value_min,
                })
            elif filter_value_max:
                queryset = queryset.filter(**{
                    f"{field_name}__lte": filter_value_max,
                })

        return queryset
