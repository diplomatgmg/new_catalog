from django.contrib import admin

from apps.review.models import CPUReview, GPUReview


class BaseAdminReview(admin.ModelAdmin):
    raw_id_fields = ("product",)


@admin.register(CPUReview)
class CPUReviewAdmin(BaseAdminReview):
    pass


@admin.register(GPUReview)
class GPUReviewAdmin(BaseAdminReview):
    pass
