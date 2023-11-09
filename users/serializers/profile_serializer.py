from rest_framework import serializers

from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "full_name",
            "image",
            "gender"
        )
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def update(self, instance, validated_data):
        for x, y in validated_data.items():
            setattr(instance, x, y)
        if not validated_data.get("image"):
            Profile.update_image(instance)
        return instance


class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(source="profile.full_name")
    image = serializers.ImageField(source="profile.image")

    class Meta:
        fields = ("id", "full_name", "image")
