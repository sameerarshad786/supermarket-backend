from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users.serializers import (
    RegisterUserSerializer, HandleUserAuthenticationSeriaizer
)
from users.models import User


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()


class LoginAPIView(generics.GenericAPIView):
    serializer_class = HandleUserAuthenticationSeriaizer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
