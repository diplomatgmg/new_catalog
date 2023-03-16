from django.contrib import admin

from apps.product.models import Brand, Category, CPUModel


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CPUModel)
class CPUModelAdmin(admin.ModelAdmin):
    list_select_related = ('brand',)
