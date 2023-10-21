from django.contrib import admin
from .models import Product, Type, Cart, CartItem


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "brand",
        "source",
        "created",
        "updated"
    )


@admin.register(Type)
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
