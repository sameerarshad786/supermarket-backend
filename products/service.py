from products.models import Product
from products.spiders import DarazProductDetailSpider, EbayProductDetailSpider


def filtered_paginated_response(self, queryset):
    queryset = self.filter_queryset(self.queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.serializer_class(
        page, context={"request": self.request}, many=True
    )
    data = self.get_paginated_response(serializer.data).data
    return data


async def reload_product(product: Product):
    if product.by == Product.By.DARAZ:
        await DarazProductDetailSpider(
            product
        ).start_request(product.url)
    elif product.by == Product.By.EBAY:
        await EbayProductDetailSpider(
            product
        ).start_request(product.url)


def union(lst1, lst2):
    # https://www.geeksforgeeks.org/python-union-two-lists/
    final_list = list(set(lst1) | set(lst2))
    return final_list
