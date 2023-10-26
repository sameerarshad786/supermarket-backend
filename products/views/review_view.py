from products.serializers import ReviewSerializer
from products.models import Review

from rest_framework import generics, parsers


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    parser_classes = (parsers.MultiPartParser, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("product_id")
        return context
