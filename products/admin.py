from django.contrib import admin
from .models import Products, ProductTypes


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "brand",
        "source",
        "created",
        "updated"
    )


@admin.register(ProductTypes)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "valid_name"
    )
