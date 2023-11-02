from rest_framework import serializers

from products.models import Store
from products.serializers import TypeSerializer, ProductSerializer
from users.serializers import UserSerializer


class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(many=True)

    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "type",
            "url",
            "main_photo",
            "cover_photo",
            "product",
            "user"
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
            fields["type"] = TypeSerializer()
        if self.context.get("show_products", False) is False:
            fields.pop("product")
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        return Store.objects.create(user=user, **validated_data)
