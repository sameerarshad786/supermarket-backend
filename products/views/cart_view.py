from rest_framework import generics, status
from rest_framework.response import Response

from products.models import CartItem
from products.serializers import CartSerializer, CartItemSerializer


class CartAPIView(generics.GenericAPIView):
    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            instance=request.user.cart,
            context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = "product_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_id")
        return context


class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = "product_id"
    allowed_methods = ["PATCH"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_id")
        return context


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = "product_id"
