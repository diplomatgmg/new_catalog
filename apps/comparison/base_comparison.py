from mixins.ListViewMixin import ListViewMixin
from mixins.TemplateViewMixin import TemplateViewMixin


class BaseComparisonListView(ListViewMixin, TemplateViewMixin):
    template_name = "comparison/product-list.html"
    context_object_name = "comparison_list"
    comparison_fields = ()
    object_list = None
    model = None

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
        context["comparison_objects"] = self.object_list
        return context
