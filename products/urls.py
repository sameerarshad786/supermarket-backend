from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.ProductsListAPIView.as_view(), name="products-list"),
    path(
        "retrieve/<uuid:id>/",
        views.ProductRetrieveAPIView.as_view(),
        name="product-details"
    ),
    path(
        "create/",
        views.ProductCreateAPIView.as_view(),
        name="create-product"
    ),
    path(
        "update/<uuid:id>/",
        views.ProductUpdateAPIView.as_view(),
        name="update-product"
    )
]
