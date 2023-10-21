from rest_framework import serializers

from ..models.product_model import Product, Type
from .serializer_fields import DecimalRangeFieldSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("id", "type")


class ProductSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    on_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "price",
            "brand",
            "condition",
            "discount",
            "source",
            "url",
            "on_cart"
        ]

    def get_fields(self):
        product_id = self.context.get("product_id")
        fields = super().get_fields()
        if product_id:
            fields.update({
                "description": serializers.CharField(),
                "items_sold": serializers.IntegerField(),
                "ratings": serializers.IntegerField(),
                "original_price": serializers.DecimalField(
                    max_digits=7, decimal_places=2),
                "discount": serializers.IntegerField(),
                "shipping_charges": serializers.DecimalField(
                    max_digits=5, decimal_places=2),
                "meta": serializers.JSONField()
            })
        else:
            fields.update({
                "detail": serializers.HyperlinkedIdentityField(
                    view_name="product-details",
                    lookup_field="id"
                )
            })
        return fields

    def get_on_cart(self, obj):
        user = self.context["request"].user
        return user.cart.cart_item.filter(product_id=obj.id).exists()
