# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy

from decimal import Decimal

from psycopg2.extras import NumericRange

from products.models import Category, Brand, Product


class ProductsItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    images = scrapy.Field()
    ratings = scrapy.Field()
    items_sold = scrapy.Field()
    condition = scrapy.Field()
    original_price = scrapy.Field()
    price = scrapy.Field()
    shipping_charges = scrapy.Field()
    by = scrapy.Field()
    discount = scrapy.Field()
    available = scrapy.Field()
    meta = scrapy.Field()

    async def get_brand(self, brand):
        brand = brand.replace("_", "")
        if "," in brand:
            brand = brand.split(",")[0]
        try:
            instance = await Brand.objects.aget(name__icontains=brand)
        except Brand.DoesNotExist:
            instance = await Brand.objects.acreate(name=brand.capitalize())
        except Brand.MultipleObjectsReturned:
            instance = await Brand.objects.filter(
                name__icontains=brand).afirst()

        return instance

    def get_price(self, price: list):
        if len(price) == 1:
            return NumericRange(Decimal(price[0]))
        elif not price:
            return None
        else:
            return NumericRange(Decimal(price[0]), Decimal(price[1]))

    def get_ratings(self, ratings):
        if ratings:
            return Decimal(re.sub(r"[^\d.]", "", ratings[0]))
        else:
            return 0.00

    def get_shipping_charges(self, shipping):
        shipping_ = re.sub(r"[^\d.]", "", shipping)
        return shipping_ if shipping_ != '' else 0

    def calc_discount(self, price, original_price):
        if original_price:
            original_price = Decimal(original_price)
            price = Decimal(price[0])
            return ((original_price-price)/original_price)*100
        return 0

    async def get_category(self, sub_category, category=None):
        if category:
            try:
                category = await Category.objects.aget(
                    name__icontains=category)
            except Category.DoesNotExist:
                category = await Category.objects.acreate(name=category)

        if sub_category:
            try:
                sub_category = await Category.objects.aget(
                    sub_category=category,
                    name__icontains=sub_category
                )
            except Category.DoesNotExist:
                sub_category = await Category.objects.acreate(
                    sub_category=category,
                    name=sub_category
                )
            return sub_category
        return sub_category

    def get_condition(self, condition):
        for value in Product.Condition:
            if value._value_ in condition.lower():
                return value._value_
        return Product.Condition.NOT_DEFINED
