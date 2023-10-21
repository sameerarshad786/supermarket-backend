from rest_framework import generics, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from elasticsearch.exceptions import ConnectionError

from products.models import Products
from products.serializers import ProductSerializer
from products.documents import ProductDocument
from products.pagination import StandardResultsSetPagination
from products.filters import ProductsFilter


class ProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter
    queryset = Products.objects.all().order_by("-created_at", "-updated_at")

    def list(self, request, *args, **kwargs):
        search = self.request.GET.get("search")
        condition = self.request.GET.get("condition")
        brand = self.request.GET.get("brand")
        source = self.request.GET.get("source")
        price = self.request.GET.get("price")
        page = int(self.request.GET.get("page", 1))
        page_size = int(self.request.GET.get("page_size", 10))

        try:
            queryset = ProductDocument.search_product_using_es(
                search,
                condition,
                brand,
                source,
                price,
                page,
                page_size
            )
            next_page = page + 1 if page * page_size < queryset["hits"]["total"]["value"] else None # noqa
            if page != 1:
                next = "{}".format(
                    request.build_absolute_uri().replace(
                        str(page), str(next_page)
                    )
                )
            else:
                next = "{}?page={}".format(
                    request.build_absolute_uri(), next_page)

            if page > 1:
                previous = "{}".format(
                    request.build_absolute_uri().replace(
                        str(page), str(page-1)
                    )
                )
            else:
                previous = None
            serializer = self.serializer_class(
                queryset,
                context={"request": request, "is_elasticsearch": True},
                many=True
            )
            data = {
                "count": queryset["hits"]["total"]["value"],
                "next": next,
                "previous": previous,
                "results": serializer.data
            }
        except ConnectionError:
            queryset = self.filter_queryset(self.queryset)
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(
                page, context={"request": request}, many=True
            )
            data = self.get_paginated_response(serializer.data).data

        return Response(data, status=status.HTTP_200_OK)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("id")
        return context


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    allowed_methods = ["PATCH"]
