from django.contrib import admin

from apps.product.models import Brand, Category, CPUModel, GPUModel


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


class BaseProductModelAdmin(admin.ModelAdmin):
    search_fields = ("slug",)
    list_select_related = ("brand",)


@admin.register(CPUModel)
class CPUModelAdmin(BaseProductModelAdmin):
    pass


@admin.register(GPUModel)
class GPUModelAdmin(BaseProductModelAdmin):
    pass
