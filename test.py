# from django.core.paginator import Paginator
# from django.shortcuts import render
# from django.views.generic import ListView
#
#
# class BaseProductListView(ListView):
#     object_list = None
#     template_name = "product/product-list.html"
#     context_object_name = "products"
#     range_filter_fields = ()
#     choice_filter_fields = ()
#     list_display_fields = ()
#     brief_list = ()
#     paginate_by = 73
#
#     def is_ajax(self):
#         return (
#             self.request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
#         )
#
#     def get(self, request, *args, **kwargs):
#         if self.is_ajax():
#             self.object_list = self.get_queryset()
#
#             paginator = Paginator(self.object_list, self.paginate_by)
#             page_number = self.request.GET.get("page")
#             page_obj = paginator.get_page(page_number)
#
#             context = self.get_context_data(object_list=self.object_list)
#             context["products"] = page_obj.object_list
#
#             return render(request, "product/products.html", context)
#         else:
#             return super().get(request, *args, **kwargs)
#
#     def get_queryset(self):
#         query = self.request.GET.get("q")
#         queryset = self.model.objects.all().select_related("brand", "category")
#
#         if query:
#             query = ".*" + " ".join(query.lower().strip().split()) + ".*"
#             query_new = query.replace(" ", ".")
#             queryset_new = queryset.filter(slug__iregex=query_new)
#             if not queryset_new:
#                 query_new = query.replace(" ", ".+")
#                 queryset_new = queryset.filter(slug__iregex=query_new)
#             if queryset_new:
#                 queryset = queryset_new
#
#         brand = self.request.GET.getlist("brand")
#         if brand:
#             queryset = queryset.filter(brand__name__in=brand)
#
#         for field_name in self.range_filter_fields:
#             filter_value_min = self.request.GET.get(f"{field_name}_min")
#             filter_value_max = self.request.GET.get(f"{field_name}_max")
#             filter_kwargs = {}
#             if filter_value_min:
#                 filter_kwargs[f"{field_name}__gte"] = filter_value_min
#             if filter_value_max:
#                 filter_kwargs[f"{field_name}__lte"] = filter_value_max
#             if filter_kwargs:
#                 queryset = queryset.filter(**filter_kwargs)
#
#         for field in self.choice_filter_fields:
#             if field not in ("brand",):
#                 value = self.request.GET.getlist(field)
#                 if not value:
#                     value = self.request.GET.getlist(f"{field}[]")
#                 if value:
#                     queryset = queryset.filter(**{f"{field}__in": value})
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context["range_filter_fields"] = self.range_filter_fields
#         context["choice_filter_fields"] = self.choice_filter_fields
#         context["list_display_fields"] = self.list_display_fields
#         context["brief_list"] = self.brief_list
#
#         context["context"] = {}
#         context["context"]["brand"] = sorted(
#             set(product.brand.name for product in self.object_list)
#         )
#
#         if self.object_list.exists():
#             for field_name in self.choice_filter_fields:
#                 if field_name not in ("brand",):
#                     context["context"][field_name] = sorted(
#                         set(
#                             getattr(product, field_name)
#                             for product in self.object_list
#                             if getattr(product, field_name) is not None
#                         )
#                     )
#
#             for field_name in self.range_filter_fields:
#                 context["context"][f"{field_name}_min"] = min(
#                     getattr(product, field_name)
#                     for product in self.object_list
#                     if getattr(product, field_name) is not None
#                 )
#                 context["context"][f"{field_name}_max"] = max(
#                     getattr(product, field_name)
#                     for product in self.object_list
#                     if getattr(product, field_name) is not None
#                 )
#
#         return context
#
#


class A:
    name = "name"
    last_name = "last_name"

    def get_full_name(self):
        return self.name + " " + self.last_name


a = A()
print(a.get_full_name)
