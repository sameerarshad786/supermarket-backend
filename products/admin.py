from django.contrib import admin
from django import forms

from . import models


@admin.register(models.Product)
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


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "valid_name"
    )


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created",
        "updated"
    )


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity")


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product_id", "rating")


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created", "updated")


class MyCustomInlineForm(forms.ModelForm):
    name = forms.CharField(label='First Param', required=False)
    description = forms.CharField(label='Second Param', required=False)


class RulesAdmin(admin.StackedInline):
    model = models.Rules
    extra = 1
    form = MyCustomInlineForm


class ProductScraperAdmin(admin.ModelAdmin):
    inlines = [RulesAdmin]


admin.site.register(models.ProductScraper, ProductScraperAdmin)
