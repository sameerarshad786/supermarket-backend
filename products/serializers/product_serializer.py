from rest_framework import serializers

from products.models import Product, Type
from .serializer_fields import DecimalRangeFieldSerializer
from .review_serializer import ReviewSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("id", "type")

    def create(self, validated_data):
        type = validated_data.get("type").capitalize()
        return Type.objects.create(type=type)


class ProductSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    on_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "images",
            "price",
            "ratings",
            "brand",
            "condition",
            "discount",
            "by",
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
                "original_price": serializers.DecimalField(
                    max_digits=7, decimal_places=2),
                "html": serializers.CharField(),
                "store": serializers.SerializerMethodField(),
                "shipping_charges": serializers.DecimalField(
                    max_digits=5, decimal_places=2),
                "reviews": serializers.SerializerMethodField(),
                "meta": serializers.JSONField(),
                "reload": serializers.HyperlinkedIdentityField(
                    view_name="reload",
                    lookup_field="id"
                )
            })
        else:
            fields.update({
                "detail": serializers.HyperlinkedIdentityField(
                    view_name="product-details",
                    lookup_field="id"
                )
            })
        return fields

    def get_reviews(self, obj):
        return ReviewSerializer(
            obj.review_set.all(),
            context={**self.context},
            many=True
        ).data

    def get_store(self, obj):
        if obj.store_set.exists():
            from products.serializers import StoreSerializer
            return StoreSerializer(
                obj.store_set.get(),
                context={**self.context},
            ).data
        return {}

    def get_on_cart(self, obj):
        user = self.context["request"].user
        return user.cart.cart_item.filter(product_id=obj.id).exists()
