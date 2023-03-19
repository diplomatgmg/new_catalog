from django.contrib import admin

from apps.compare.models import CPUComparison, GPUComparison


class BaseComparisonAdmin(admin.ModelAdmin):
    list_display = ('user', 'num_products')
    search_fields = ('user__username',)
    filter_horizontal = ('products',)

    @staticmethod
    def num_products(obj):
        return obj.products.count()


@admin.register(CPUComparison)
class CPUComparisonAdmin(BaseComparisonAdmin):
    pass


@admin.register(GPUComparison)
class GPUComparisonAdmin(BaseComparisonAdmin):
    pass
