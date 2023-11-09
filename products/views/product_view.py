import asyncio

from rest_framework import generics, status, views, parsers
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from products.models import Product, Category
from products.serializers import ProductSerializer, ProductDataSerializer, CategorySerializer
# from products.documents import ProductDocument
from products.pagination import StandardResultsSetPagination
from products.filters import CategoryFilter, ProductsFilter
from products.service import filtered_paginated_response, reload_product


class CategorySearchAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.filter(sub_category__isnull=False)


class TypeCreateAPIView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductsListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter
    queryset = Product.objects.all().order_by("-created_at", "-updated_at")

    def list(self, request, *args, **kwargs):
        search = self.request.GET.get("search")
        condition = self.request.GET.get("condition")
        brand = self.request.GET.get("brand")
        by = self.request.GET.get("by")
        price = self.request.GET.get("price")
        page = int(self.request.GET.get("page", 1))
        page_size = int(self.request.GET.get("page_size", 10))

        # try:
        #     queryset = ProductDocument.search_product_using_es(
        #         search,
        #         condition,
        #         brand,
        #         by,
        #         price,
        #         page,
        #         page_size
        #     )
        #     next_page = page + 1 if page * page_size < queryset["hits"]["total"]["value"] else None # noqa
        #     if page != 1:
        #         next = "{}".format(
        #             request.build_absolute_uri().replace(
        #                 str(page), str(next_page)
        #             )
        #         )
        #     else:
        #         next = "{}?page={}".format(
        #             request.build_absolute_uri(), next_page)

        #     if page > 1:
        #         previous = "{}".format(
        #             request.build_absolute_uri().replace(
        #                 str(page), str(page-1)
        #             )
        #         )
        #     else:
        #         previous = None
        #     serializer = self.serializer_class(
        #         queryset,
        #         context={"request": request, "is_elasticsearch": True},
        #         many=True
        #     )
        #     data = {
        #         "count": queryset["hits"]["total"]["value"],
        #         "next": next,
        #         "previous": previous,
        #         "results": serializer.data
        #     }
        # except ConnectionError:
        data = filtered_paginated_response(self, self.queryset)

        return Response(data, status=status.HTTP_200_OK)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProductDataSerializer
    queryset = Product.objects.all()


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductDataSerializer
    queryset = Product.objects.all()
    parser_classes = (parsers.MultiPartParser, )
    schema = None


class ProductReloadAPIView(views.APIView):
    serializer_class = ProductDataSerializer

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))

    def put(self, request, *args, **kwargs):
        asyncio.run(reload_product(self.get_object()))
        serializer = self.serializer_class(
            instance=self.get_object(),
            context={
                "request": request,
                "product_id": self.kwargs.get("id")
            }
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
