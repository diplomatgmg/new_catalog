from django.shortcuts import render
from django.views.generic import ListView


class BaseProductListView(ListView):
    object_list = None
    model = None
    template_name = "product/product-list.html"
    context_object_name = "products"
    range_filter_fields = ()
    choice_filter_fields = ()
    list_display_fields = ()
    brief_list = ()
    paginate_by = 70

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if self.is_ajax():
            return self.ajax()

        return self.render_to_response(context)

    def ajax(self):
        context = self.get_context_data()
        return render(self.request, "product/products.html", context)

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context=context,
            **response_kwargs,
        )

    @staticmethod
    def parse_query(query, queryset):
        default_regex_query = f'.*{" ".join(query.lower().strip().split())}.*'
        regex_query = default_regex_query.replace(" ", ".")
        queryset_new = queryset.filter(slug__iregex=regex_query)
        if not queryset_new.exists():
            regex_query = default_regex_query.replace(" ", ".+")
            queryset_new = queryset.filter(slug__iregex=regex_query)
        if not queryset_new.exists():
            return queryset
        return queryset_new

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = self.model.objects.all()

        if query:
            queryset = self.parse_query(query, queryset)

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

        for field in self.choice_filter_fields:
            if field not in ("brand",):
                value = self.request.GET.getlist(field)
                if not value:
                    value = self.request.GET.getlist(f"{field}[]")
                if value:
                    queryset = queryset.filter(**{f"{field}__in": value})

        return queryset

    def queryset_paginate(self, queryset):
        page = int(self.kwargs.get("page") or self.request.GET.get("page") or 1)
        size = self.paginate_by
        start = (page - 1) * size
        end = start + size
        return queryset[start:end]

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset().select_related("brand", "category")

        context = {
            "range_filter_fields": self.range_filter_fields,
            "choice_filter_fields": self.choice_filter_fields,
            "list_display_fields": self.list_display_fields,
            "brief_list": self.brief_list,
            "context": {},
        }

        context["context"]["brand"] = sorted(
            set(product.brand.name for product in queryset)
        )

        if queryset.exists():
            for field_name in self.choice_filter_fields:
                if field_name not in ("brand",):
                    context["context"][field_name] = set(
                        getattr(product, field_name)
                        for product in queryset
                        if getattr(product, field_name) is not None
                    )

            for field_name in self.range_filter_fields:
                context["context"][f"{field_name}_min"] = min(
                    getattr(product, field_name)
                    for product in queryset
                    if getattr(product, field_name) is not None
                )
                context["context"][f"{field_name}_max"] = max(
                    getattr(product, field_name)
                    for product in queryset
                    if getattr(product, field_name) is not None
                )

        queryset = self.queryset_paginate(queryset)
        context["products"] = queryset

        return context

    def is_ajax(self):
        return (
            self.request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        )
