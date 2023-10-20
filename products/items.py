# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy

from decimal import Decimal

from psycopg2.extras import NumericRange

from products.models import Products, ProductTypes


class ProductsItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    type = scrapy.Field()
    image = scrapy.Field()
    ratings = scrapy.Field()
    items_sold = scrapy.Field()
    condition = scrapy.Field()
    original_price = scrapy.Field()
    price = scrapy.Field()
    shipping_charges = scrapy.Field()
    source = scrapy.Field()
    discount = scrapy.Field()

    def get_brand(self, brand):
        if brand:
            brand_names = [condition.value for condition in Products.Brand]
            brand = brand.lower().split(" ")[0]
            brand = brand_names.index(brand)
            return brand_names[brand]
        else:
            return brand[0]

    def get_price(self, price: list):
        if len(price) == 1:
            return NumericRange(Decimal(price[0]))
        else:
            return NumericRange(Decimal(price[0]), Decimal(price[1]))

    def get_ratings(self, ratings):
        if ratings:
            return Decimal(re.sub(r"[^\d.]", "", ratings[0]))
        else:
            return 0.00

    def get_shipping_charges(self, shipping):
        if list(filter(lambda x: re.search(r"\d", x), shipping)):
            return Decimal(re.sub(r"[^\d.]", "", shipping[0]))
        else:
            return 0.00

    def calc_discount(self, price, original_price):
        if original_price:
            price = Decimal(price[0])
            return ((original_price-price)/original_price)*100
        return 0

    async def get_type(self, type):
        try:
            instance = await ProductTypes.objects.aget(type__icontains=type)
        except ProductTypes.DoesNotExist:
            instance = await ProductTypes.objects.acreate(type=type)

        return instance
