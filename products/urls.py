from django.urls import path, include

from . import views


TYPE_URL_PATTERNS = [
    path("search/", views.SearchTypeAPIView.as_view(), name="search-type"),
    path("create/", views.TypeCreateAPIView.as_view(), name="create-type")
]


PRODUCT_URL_PATTERNS = [
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
    )
]


CART_URL_PATTERNS = [
    path("list/", views.CartAPIView.as_view(), name="user-cart"),
    path(
        "add-to-cart/<uuid:product_id>/",
        views.CartItemCreateAPIView.as_view(),
        name="add-to-cart"
    ),
    path(
        "update-cart-item/<uuid:product_id>",
        views.CartItemUpdateAPIView.as_view(),
        name="update-cart-item"
    ),
    path(
        "remove-from-cart/<uuid:product_id>",
        views.CartItemDeleteAPIView.as_view(),
        name="remove-from-cart"
    )
]


urlpatterns = [
    path("type/", include(TYPE_URL_PATTERNS)),
    path("products/", include(PRODUCT_URL_PATTERNS)),
    path("carts/", include(CART_URL_PATTERNS))
]
