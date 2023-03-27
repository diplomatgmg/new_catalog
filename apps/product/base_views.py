from urllib.parse import urlencode

from django.http import QueryDict
from django.shortcuts import redirect, render
from django.views.generic import DetailView, TemplateView


class BaseProductListView(TemplateView):
    query = {}
    object_list = None
    model = None
    template_name = "product/product-list.html"
    context_object_name = "products"
    range_filter_fields = ()
    choice_filter_fields = {}
    list_display_fields = ()
    brief_list = ()
    paginate_by = 40

    def get(self, request, *args, **kwargs):
        redirect_path = self.find_query_to_redirect()
        if redirect_path:
            return redirect(redirect_path)

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
    def clear_query(query):
        return " ".join(query.lower().strip().split())

    def find_query_to_redirect(self):
        request = self.request

        query = request.GET.get("q")

        if query:
            self.query["q"] = query
        else:
            meta = request.META.get("HTTP_REFERER")
            query_string = request.META.get("QUERY_STRING")
            if meta and "?" in meta and query_string:
                query_dict = QueryDict(meta.split("?")[-1])
                query = query_dict.get("q")
                if query:
                    path = request.path
                    new_query = urlencode({"q": query})
                    redirect_path = f"{path}?{new_query}&{query_string}"
                    return redirect_path
        return False

    def parse_query(self, query, queryset):
        default_regex_query = f".*{self.clear_query(query)}.*"
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
        page = int(self.request.GET.get("page", 1))
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
            for field_name, lambda_sort in self.choice_filter_fields.items():
                if field_name not in ("brand",):
                    fields = set(
                        getattr(product, field_name)
                        for product in queryset
                        if getattr(product, field_name) is not None
                    )
                    if lambda_sort:
                        fields = sorted(fields, key=lambda_sort)
                    context["context"][field_name] = fields

            for field_name in self.range_filter_fields:
                context["context"][f"{field_name}_min"] = min(
                    (
                        getattr(product, field_name)
                        for product in queryset
                        if getattr(product, field_name) is not None
                    ),
                    default=None,
                )
                context["context"][f"{field_name}_max"] = max(
                    (
                        getattr(product, field_name)
                        for product in queryset
                        if getattr(product, field_name) is not None
                    ),
                    default=None,
                )

        queryset = self.queryset_paginate(queryset)
        context["products"] = queryset

        return context

    def is_ajax(self):
        return (
            self.request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        )


class BaseProductDetailView(DetailView):
    template_name = "product/product-detail.html"
    object = None
    list_display_fields = ()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get("slug")
        queryset = queryset.filter(slug=slug)
        try:
            return queryset.get()
        except queryset.model.DoesNotExist:
            return []

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = {
            "product": self.object,
            "list_display_fields": self.list_display_fields,
        }

        return context

    def render_to_response(self, context, **response_kwargs):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context=context,
            **response_kwargs,
        )
