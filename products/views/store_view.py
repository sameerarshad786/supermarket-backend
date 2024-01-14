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
    search_fields = ["id", "name"]


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class StoreRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["show_products"] = True
        return context


class StoreUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    allowed_methods = ["PATCH"]
    permission_classes = [IsObjectPermission]


class StoreDeleteAPIView(generics.DestroyAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = [IsObjectPermission]
