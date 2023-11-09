from django.contrib import admin
from .models import Product, Category, Brand, Cart, CartItem, Review, Store


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_name",
        "by",
        "ratings",
        "brand_name",
        "created",
        "updated"
    )
    search_fields = ("id", )

    def brand_name(self, obj):
        return obj.brand.name


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "valid_name"
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created",
        "updated"
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
