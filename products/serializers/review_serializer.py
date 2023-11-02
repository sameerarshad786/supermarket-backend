from django.conf import settings

from rest_framework import serializers

from products.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    by = serializers.CharField(
        default=Review.Source.CURRENT, read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "name",
            "rating",
            "review",
            "by",
            "user",
            "images"
        )
        extra_kwargs = {
            "product": {"read_only": True},
            "name": {"read_only": True}
        }

    def get_fields(self):
        name = self.context["request"].resolver_match.url_name
        name_list = ["reload", "product-details"]
        fields = super().get_fields()
        if name not in name_list:
            fields["images"] = serializers.ListField(
                child=serializers.FileField(required=False),
                required=False
            )
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        images = []
        product_id = self.context["product_id"]
        for image in validated_data.pop("images"):
            with open(f"media/reviews/{image}", 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
                    images.append(f.name)

        review = Review.objects.create(
            user=user,
            images=images,
            product_id=product_id,
            **validated_data
        )
        return review

    def to_representation(self, instance: Review):
        representation = super().to_representation(instance)
        images = []
        if instance.source == Review.Source.CURRENT and instance.images:
            images = list(
                map(lambda x: f"{settings.FRONTEND_URL}{x}", instance.images)
            )
            representation["images"] = images
        return representation
