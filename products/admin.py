from django.contrib import admin
from .models import Product, Type, Cart, CartItem, Review, Store


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "by",
        "brand",
        "created",
        "updated"
    )
    search_fields = ("id", )


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "valid_name"
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product_id", "rating")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created", "updated")
