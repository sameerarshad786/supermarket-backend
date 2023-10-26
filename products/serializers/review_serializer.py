from django.conf import settings

from rest_framework import serializers

from products.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = serializers.ListField(
        child=serializers.FileField(required=False),
        required=False
    )
    source = serializers.CharField(default=Review.Sources.CURRENT, read_only=True)

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
            "product": {"read_only": True},
            "name": {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context["request"].user
        images = []
        product_id = self.context["product_id"]
        for image in validated_data.pop("images"):
            with open(f"media/reviews/{image}", 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                    images.append(
                        "{}{}".format(
                            settings.FRONTEND_URL,
                            f.name
                        )
                    )
        return Review.objects.create(
            user=user,
            images=images,
            product_id=product_id,
            **validated_data
        )
