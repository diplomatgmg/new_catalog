from django.views.generic import ListView


class BaseProductListView(ListView):
    template_name = "product/product-list.html"
    context_object_name = "products"
    range_filter_fields = ()
    search_filter_fields = ()
    list_display_fields = ()
    brief_list = ()

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = self.model.objects.all().select_related("brand")

        if query:
            query = ".*" + " ".join(query.lower().strip().split()) + ".*"
            query_new = query.replace(" ", ".")
            queryset_new = queryset.filter(slug__iregex=query_new)
            if not queryset_new:
                query_new = query.replace(" ", ".+")
                queryset_new = queryset.filter(slug__iregex=query_new)
            if queryset_new:
                queryset = queryset_new

        brand = self.request.GET.getlist("brand")
        if brand:
            queryset = queryset.filter(brand__name__in=brand)

        for field_name in self.range_filter_fields:
            filter_value_min = self.request.GET.get(f"{field_name}_min")
            filter_value_max = self.request.GET.get(f"{field_name}_max")
            filter_kwargs = {}
            if filter_value_min:
                filter_kwargs[f"{field_name}__gte"] = filter_value_min
            if filter_value_max:
                filter_kwargs[f"{field_name}__lte"] = filter_value_max
            if filter_kwargs:
                queryset = queryset.filter(**filter_kwargs)

        for field in self.search_filter_fields:
            if field not in ("brand",):
                value = self.request.GET.getlist(field)
                if value:
                    queryset = queryset.filter(**{f"{field}__in": value})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["range_filter_fields"] = self.range_filter_fields
        context["search_filter_fields"] = self.search_filter_fields
        context["list_display_fields"] = self.list_display_fields
        context["brief_list"] = self.brief_list

        context["context"] = {}
        context["context"]["brand"] = sorted(
            set(product.brand.name for product in self.object_list)
        )

        if self.object_list.exists():
            for field_name in self.search_filter_fields:
                if field_name not in ("brand",):
                    context["context"][field_name] = sorted(
                        set(
                            getattr(product, field_name)
                            for product in self.object_list
                        )
                    )

            for field_name in self.range_filter_fields:
                context["context"][f"{field_name}_min"] = min(
                    getattr(product, field_name) for product in self.object_list
                )
                context["context"][f"{field_name}_max"] = max(
                    getattr(product, field_name) for product in self.object_list
                )

        return context
