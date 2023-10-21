from rest_framework import serializers

from products.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "name", "star", "review", "source", "user", "product")
        extra_kwargs = {
            "product": {"read_only": True}
        }
