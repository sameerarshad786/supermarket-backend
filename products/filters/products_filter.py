from django_filters import rest_framework as filters

from products.models import Product
from .filter_fields import DecimalRangeFilter


class ProductsFilter(filters.FilterSet):
    search = filters.CharFilter(method='get_search')
    price = DecimalRangeFilter()

    class Meta:
        model = Product
        fields = ("search", "condition", "brand", "source", "price")

    def get_search(self, queryset, name, value):
        queryset = queryset.filter(
            name__icontains=value
        )
        return queryset
