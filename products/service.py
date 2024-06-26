from products.models import Product
from products.spiders import details


def filtered_paginated_response(self, queryset):
    queryset = self.filter_queryset(self.queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.serializer_class(
        page, context={"request": self.request}, many=True
    )
    data = self.get_paginated_response(serializer.data).data
    return data


async def reload_product(product: Product):
    class_name = f"{product.by.capitalize()}ProductDetailSpider"
    spider = getattr(details, class_name)
    await spider(product).start_request(product.url)


def union(lst1, lst2):
    # https://www.geeksforgeeks.org/python-union-two-lists/
    final_list = list(set(lst1) | set(lst2))
    return final_list
