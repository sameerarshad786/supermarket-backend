from django.contrib import admin

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


@admin.register(models.ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_id")


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created", "updated")


class ExtractorInline(admin.TabularInline):
    model = models.Extractor
    extra = 0


class RuleInline(admin.TabularInline):
    model = models.Rule
    extra = 0
    inlines = ExtractorInline


@admin.register(models.ProductScraper)
class ScraperAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "updated")
    inlines = [RuleInline]


# @admin.register(models.Extractor)
class ExtractorAdmin(admin.ModelAdmin):
    list_display = ("id", "extractor_type", "pattern")

admin.site.register(models.Extractor, ExtractorAdmin)

@admin.register(models.Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ("id", "field_name", "product_scraper_id")
