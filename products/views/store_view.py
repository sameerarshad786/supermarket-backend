from rest_framework import generics, filters

from products.models import Store
from products.serializers import StoreSerializer


class SearchStoreAPIView(generics.ListAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class StoreCreateAPIView(generics.CreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class StoreUpdateAPIView(generics.UpdateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    allowed_methods = ["PATCH"]


class StoreDeleteAPIView(generics.DestroyAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)
