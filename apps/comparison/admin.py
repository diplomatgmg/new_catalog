from django.contrib import admin

from apps.comparison.models import CPUComparison, GPUComparison


class BaseComparisonAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)
    filter_horizontal = ("products",)

    @staticmethod
    def num_products(obj):
        return obj.products.count()


@admin.register(CPUComparison)
class CPUComparisonAdmin(BaseComparisonAdmin):
    pass


@admin.register(GPUComparison)
class GPUComparisonAdmin(BaseComparisonAdmin):
    pass
