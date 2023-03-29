from apps.review.forms import ReviewForm
from mixins.mixins import CreateViewMixin, ListViewMixin, TemplateViewMixin
from services.services import (
    find_product_model_by_slug,
    find_review_model_by_slug,
    get_product_by_slug,
)


class ReviewListCreateView(ListViewMixin, CreateViewMixin, TemplateViewMixin):
    template_name = "review/product-review.html"
    context_object_name = "reviews"
    form_class = ReviewForm
    product_model = None
    product = None
    review_model = None
    review_products = None

    def dispatch(self, request, *args, **kwargs):
        self.review_model = self.get_review_model()
        self.review_products = self.get_review_products()
        self.product_model = self.get_product_model()
        self.product = self.get_product()
        return super().dispatch(request, *args, **kwargs)

    def get_review_model(self):
        category_slug = self.kwargs.get("category_slug")
        review_model = find_review_model_by_slug(category_slug)
        return review_model

    def get_review_products(self):
        product_slug = self.kwargs.get("product_slug")
        return self.review_model.objects.filter(product__slug=product_slug)

    def get_product_model(self):
        category_slug = self.kwargs.get("category_slug")
        product_model = find_product_model_by_slug(category_slug)
        return product_model

    def get_product(self):
        product_slug = self.kwargs.get("product_slug")
        product = get_product_by_slug(self.product_model, product_slug)
        return product

    def get_queryset(self):
        queryset = self.review_products
        return queryset.select_related("user")

    def form_valid(self, form):
        self.review_model.objects.create(
            user=self.request.user,
            product=self.product,
            **form.cleaned_data,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path
