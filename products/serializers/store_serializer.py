from django.conf import settings

from rest_framework import serializers

from products.models import Store
from products.serializers import CategorySerializer, ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()
    product = ProductSerializer(many=True)

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "category",
            "url",
            "main_photo",
            "cover_photo",
            "total_products",
            "product"
        )
        extra_kwargs = {
            "product": {"required": False}
        }

    def get_fields(self):
        fields = super().get_fields()
        method = self.context["request"].method
        if method == "PATCH":
            fields["name"].required = False
        if method == "GET":
            fields["category"] = CategorySerializer()
        if self.context.get("show_products", False) is False:
            fields.pop("product")
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        return Store.objects.create(user=user, **validated_data)

    def get_total_products(self, obj):
        return obj.product.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.cover_photo.startswith("http"):
            representation["cover_photo"] = f"{settings.FRONTEND_URL}media/{instance.cover_photo}" # noqa
        if not instance.main_photo.startswith("http"):
            representation["main_photo"] = f"{settings.FRONTEND_URL}media/{instance.main_photo}" # noqa
        return representation
