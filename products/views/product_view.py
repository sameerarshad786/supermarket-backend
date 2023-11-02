from django.conf import settings

from rest_framework import generics, status, views
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from elasticsearch.exceptions import ConnectionError
from scrapyd_api import ScrapydAPI

from products.models import Product, Type
from products.serializers import ProductSerializer, TypeSerializer
from products.documents import ProductDocument
from products.pagination import StandardResultsSetPagination
from products.filters import TypeFilter, ProductsFilter
from products.service import filtered_paginated_response, reload_product


class SearchTypeAPIView(generics.ListAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TypeFilter


class TypeCreateAPIView(generics.CreateAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


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
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product_id"] = self.kwargs.get("id")
        return context


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductReloadAPIView(views.APIView):
    serializer_class = ProductSerializer

    def get_object(self):
        return Product.objects.get(id=self.kwargs.get("id"))

    def put(self, request, *args, **kwargs):
        try:
            job = reload_product(self.get_object())
            _scrapyd = ScrapydAPI(settings.SCRAPYD_HOST)
            while True:
                job_status = _scrapyd.job_status("products", job)
                if job_status == "finished":
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
                elif job_status == "pending" or job_status == "running":
                    import time
                    time.sleep(3)
                else:
                    return Response(
                        {"message": "Job failed or unknown status"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            print(e)
            return Response(
                {"error": "request failed!"},
                status=status.HTTP_400_BAD_REQUEST
            )
