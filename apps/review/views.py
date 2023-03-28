from django.views.generic import TemplateView


class CPUReviewCreateView(TemplateView):
    template_name = "review/product-review.html"
