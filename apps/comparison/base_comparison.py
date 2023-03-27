from django.views.generic import TemplateView


class BaseComparisonListView(TemplateView):
    template_name = "comparison/product-list.html"
    context_object_name = "comparison_list"
    comparison_fields = ()
    object_list = None
    model = None

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_comparison = self.model.objects.filter(
                user=self.request.user
            ).last()
        else:
            user_comparison = self.model.objects.filter(
                temp_user=self.request.session.session_key
            ).last()
        if user_comparison:
            products = user_comparison.products.all()
            return products.select_related("brand", "category")
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comparison_fields"] = self.comparison_fields
        context["comparison_list"] = self.object_list
        return context
