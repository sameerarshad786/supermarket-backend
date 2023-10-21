from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "gender"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def get_fields(self):
        user = self.context["request"].user
        fields = super().get_fields()
        if user.is_anonymous:
            return fields
        else:
            fields.update({
                "image": serializers.ImageField(required=False)
            })
        return fields

    def update(self, instance, validated_data):
        for x, y in validated_data.items():
            setattr(instance, x, y)
        return instance


class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(source="profile.full_name")
    image = serializers.ImageField(source="profile.image")

    class Meta:
        fields = ("id", "full_name", "image")
