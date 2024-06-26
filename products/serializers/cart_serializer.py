from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from products.models import CartItem, Cart
from .product_serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")

    def validate(self, attrs):
        product_id = self.context["product_id"]
        user = self.context["request"].user
        if user.cart.cart_item.filter(product_id=product_id).exists():
            raise serializers.ValidationError(_("Item already on cart"))
        return attrs

    def create(self, validated_data):
        product_id = self.context["product_id"]
        user = self.context["request"].user
        cart_item = CartItem.objects.create(
            product_id=product_id,
            user=user,
            **validated_data
        )
        user.cart.cart_item.add(cart_item)
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    cart_item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "cart_item")

    def get_cart_item(self, obj):
        request = self.context["request"]
        cart_item = obj.cart_item.all().order_by("-created_at")
        return CartItemSerializer(
            cart_item,
            context={"request": request},
            many=True
        ).data
