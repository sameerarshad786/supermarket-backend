from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import User
from .profile_serializer import ProfileSerializer
from users.signals import profile_values


class RegisterUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("email", "password", "profile")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        profile = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        profile_values.send(sender=User, user=user, profile=profile)
        return user


class HandleUserAuthenticationSeriaizer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=50, write_only=True
    )
    password = serializers.CharField(
        max_length=255, min_length=6, write_only=True
    )
    tokens = serializers.JSONField(
        read_only=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "tokens")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        return user
