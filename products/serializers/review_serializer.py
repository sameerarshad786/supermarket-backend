from rest_framework import serializers

from products.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "name",
            "rating",
            "review",
            "source",
            "user",
            "images"
        )
        extra_kwargs = {
            "product": {"read_only": True}
        }
