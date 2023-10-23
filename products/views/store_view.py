from rest_framework import generics, filters

from products.models import Store
from products.serializers import StoreSerializer
from products.pagination import StandardResultsSetPagination
from products.permissions import IsObjectPermission


class SearchStoreAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all().order_by("-created_at")
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class StoreUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    allowed_methods = ["PATCH"]
    permission_classes = [IsObjectPermission]


class StoreDeleteAPIView(generics.DestroyAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsObjectPermission]
