from django.contrib import admin
from .models import Products, ProductTypes, Cart, CartItem


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


@admin.register(Cart)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(CartItem)
class ProductTypesAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")
