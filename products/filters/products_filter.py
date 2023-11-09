from django_filters import rest_framework as filters

from products.models import Category, Product
from .filter_fields import DecimalRangeFilter


class CategoryFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ("category", )


class ProductsFilter(filters.FilterSet):
    search = filters.CharFilter(method='get_search')
    price = DecimalRangeFilter()

    class Meta:
        model = Product
        fields = ("search", "condition", "brand", "by", "price")

    def get_search(self, queryset, name, value):
        queryset = queryset.filter(
            name__icontains=value
        )
        return queryset
