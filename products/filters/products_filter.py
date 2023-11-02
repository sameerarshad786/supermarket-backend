from django_filters import rest_framework as filters

from products.models import Type, Product
from .filter_fields import DecimalRangeFilter


class TypeFilter(filters.FilterSet):
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")

    class Meta:
        model = Type
        fields = ("type", )


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
