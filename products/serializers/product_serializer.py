from rest_framework import serializers

from ..models.product_model import Products, ProductTypes
from .serializer_fields import DecimalRangeFieldSerializer


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = ("id", "type")


class ProductSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()

    class Meta:
        model = Products
        fields = [
            "id",
            "name",
            "image",
            "price",
            "brand",
            "condition",
            "discount",
            "source",
            "url"
        ]

    def get_fields(self):
        kwargs = self.context["request"].parser_context.get("kwargs")
        fields = super().get_fields()
        if kwargs:
            fields.update({
                "description": serializers.CharField(),
                "items_sold": serializers.IntegerField(),
                "ratings": serializers.IntegerField(),
                "original_price": serializers.DecimalField(
                    max_digits=7, decimal_places=2),
                "discount": serializers.IntegerField(),
                "shipping_charges": serializers.DecimalField(
                    max_digits=5, decimal_places=2)
            })
        else:
            fields.update({
                "detail": serializers.HyperlinkedIdentityField(
                    view_name="product-details",
                    lookup_field="id"
                )
            })
        return fields
