from rest_framework import generics, status
from rest_framework.response import Response

from users.serializers import ProfileSerializer
from users.models import Profile


class ProfileGetOrUpdateAPIView(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=self.get_object(),
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            instance=self.get_object(),
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
