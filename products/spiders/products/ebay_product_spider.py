import os
import re
import scrapy

from urllib.request import urlopen
from decimal import Decimal

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from lxml import html

from products.items import ProductsItem
from products.models import Product


class EbayProductsSpider(scrapy.Spider):
    name = Product.By.EBAY

    custom_settings = {
        "USER_AGENT": os.getenv("USER_AGENT"),
        "DEFAULT_REQUEST_HEADERS": {
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en"
        }
    }

    def start_requests(self):
        yield Request(url="https://www.ebay.com/")

    def parse(self, response, **kwargs):
        electronic_section = LinkExtractor(
            tags="a", attrs="href", restrict_text="Electronics"
        )
        _data = {}
        for data in electronic_section.extract_links(response):
            _data["url"] = data.url
            _data["type"] = data.text
        yield Request(_data["url"], callback=self.parse_electronics)

    def parse_electronics(self, response, **kwargs):
        a_elements = response.xpath("//section/div/a[div[contains(text(), 'Cell Phones, Smart Watches & Accessories')]]/@href").get() # noqa
        yield Request(a_elements, callback=self.parse_brands_products)

    # def crawl_pages(self, response, **kwargs):
    #     page_numbers = response.xpath("//ol[@class='pagination__items']/li[last()]/a/text()") # noqa
    #     if not page_numbers:
    #         print(response.text)
    #     for page in range(1, int(page_numbers)+1):
    #         current_url = response.request.url
    #         if current_url.endswith("/"):
    #             url = f"{response.request.url}?_pgn={page}"
    #         else:
    #             url = f"{response.request.url}&_pgn={page}"
    #         yield Request(url=url, callback=self.parse_brands_products)

    async def parse_brands_products(self, response, **kwargs):
        brands = (
            LinkExtractor(
                tags="a",
                attrs="href",
                restrict_xpaths="//h2[contains(text(), 'Shop by brand')]/ancestor::section" # noqa
            ).extract_links(response)
        )
        for brand in brands:
            url = urlopen(brand.url)
            page = html.fromstring(url.read(), "lxml")
            products = page.xpath(
                "//li/div[@class='s-item__wrapper clearfix']")
            for product in products:
                url = self.parse_url(product)
                name = self.parse_name(product)
                price = self.parse_price(product)
                original_price = self.parse_original_price(product)
                image = self.parse_image(product)
                items_sold = self.parse_items_sold(product)
                shipping = self.parse_shipping_charges(product)
                ratings = self.parse_ratings(product)

                item = ProductsItem()
                item["name"] = name
                item["description"] = ""
                item["brand"] = item.get_brand(brand.text)
                item["url"] = url
                item["price"] = item.get_price(price)
                item["by"] = Product.By.EBAY
                item["images"] = [image]
                item["original_price"] = original_price
                item["items_sold"] = items_sold
                item["shipping_charges"] = item.get_shipping_charges(shipping)
                item["ratings"] = ratings
                item["discount"] = item.calc_discount(price, original_price)
                item["condition"] = Product.Condition.NOT_DEFINED
                item["type"] = await item.get_type("Electronics")
                yield item

    def parse_name(self, product):
        name = product.xpath(".//a/h3[@class='s-item__title']/text() | .//a/h3[@class='s-item__title']/span/text()") # noqa
        filtered_name = list(
            filter(lambda x: x.lower() != "new listing", name))
        return filtered_name[0]

    def parse_url(self, product):
        return product.xpath(".//div/a[@class='s-item__link']/@href")[0]

    def parse_price(self, product):
        price = product.xpath(".//div/span[@class='s-item__price']/text()")
        return list(map(lambda x: re.sub(r"[^\d.]", "", x), price))

    def parse_original_price(self, product):
        original_price = product.xpath(
            ".//div/span[@class='s-item__trending-price']/span/text()"
        )
        if original_price:
            if re.search(r"\d", original_price[0]):
                return Decimal(re.sub(r"[^\d.]", "", original_price[0]))
            else:
                return 0.00
        return 0.00

    def parse_image(self, product):
        image = product.xpath(".//div[@class='s-item__image-helper']/img[@class='s-item__image-img']")[0].attrib # noqa
        try:
            image = image["data-src"]
        except KeyError:
            image = image["src"]
        return image

    def parse_items_sold(self, product):
        sold = product.xpath(
            ".//span[@class='s-item__hotness s-item__itemHotness']/span/text()"
        )
        items_sold = 0
        if sold:
            items_sold = sold[0]
            if "sold" in items_sold:
                items_sold = int(re.sub(r"[^\d.]", "", items_sold))
            else:
                items_sold = 0
        return items_sold

    def parse_shipping_charges(self, product):
        return product.xpath(
            ".//span[@class='s-item__shipping s-item__logisticsCost']/text()"
        )

    def parse_ratings(self, product):
        try:
            rating = product.xpath(
                ".//div[@class='star-rating b-rating__rating-star']/@data-stars"
            )[0]
            if "-" in rating:
                rating = rating.split("-")[0]
                rating = Decimal(rating) + Decimal(.5)
        except IndexError:
            rating = 0
        return rating
