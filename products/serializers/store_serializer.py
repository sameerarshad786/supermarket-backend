from rest_framework import serializers

from products.models import Store
from products.serializers import CategorySerializer, ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
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
