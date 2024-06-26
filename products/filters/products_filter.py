from django_filters import rest_framework as filters

from products.models import Category, Product
from .filter_fields import DecimalRangeFilter


class CategoryFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ("category", )


class ProductsFilter(filters.FilterSet):
    search = filters.CharFilter(lookup_expr="icontains", field_name="name")
    price = DecimalRangeFilter()
    category = filters.CharFilter(
        lookup_expr="icontains", field_name="category__sub_category__name"
    )

    class Meta:
        model = Product
        fields = ("search", "condition", "brand", "by", "price")
