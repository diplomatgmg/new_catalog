from django.contrib import admin

from apps.product.models import Brand, Category, CPUModel, GPUModel


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CPUModel)
class CPUModelAdmin(admin.ModelAdmin):
    list_select_related = ("brand",)


@admin.register(GPUModel)
class GPUModelAdmin(admin.ModelAdmin):
    list_select_related = ("brand",)
