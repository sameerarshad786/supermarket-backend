from django.conf import settings

from scrapyd_api import ScrapydAPI

from products.models import Product


def filtered_paginated_response(self, queryset):
    queryset = self.filter_queryset(self.queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.serializer_class(
        page, context={"request": self.request}, many=True
    )
    data = self.get_paginated_response(serializer.data).data
    return data


def reload_product(product: Product):
    _scrapyd = ScrapydAPI(settings.SCRAPYD_HOST)
    kwargs = {
        "product": product,
        "product_id": product.id,
        "url": product.url
    }
    job = _scrapyd.schedule(
        project="products",
        spider="product-details",
        **kwargs
    )
    return job
