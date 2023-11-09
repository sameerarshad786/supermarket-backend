import os
import re
import scrapy

from urllib.request import urlopen
from decimal import Decimal

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, Response
from lxml import html

from products.items import ProductsItem
from products.models import Product, Brand


class EbayProductsSpider(scrapy.Spider):
    name = Product.By.EBAY
    start_urls = ["https://www.ebay.com/"]

    custom_settings = {
        "USER_AGENT": os.getenv("USER_AGENT"),
        "DEFAULT_REQUEST_HEADERS": {
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en"
        }
    }

    def parse(self, response, **kwargs):
        categories_to_scrape = [os.getenv("EBAY_CATEGORIES")]
        for data in response.xpath("//li/a[@class='gh-ham-menu__link']"):
            for category in categories_to_scrape:
                if data.xpath("./span/text()").get() == category:
                    url = data.xpath('./@href').get()
                    kwargs["category"] = category
                    yield Request(
                        url=url,
                        callback=self.crawl_subcategories,
                        cb_kwargs=kwargs
                    )

    def crawl_subcategories(self, response, **kwargs):
        sub_categories = [os.getenv("EBAY_SUBCATEGORY")]
        sections = response.xpath("//a[@class='b-visualnav__tile b-visualnav__tile__default']")

        for section in sections:
            for sub_category in sub_categories:
                if section.xpath("./div/text()").get() == sub_category:
                    url = section.xpath("./@href").get()
                    kwargs["sub_category"] = sub_category
                    yield Request(
                        url=url,
                        callback=self.crawl_sections,
                        cb_kwargs=kwargs
                    )

    async def crawl_sections(self, response, **kwargs):
        # start = int(os.getenv("EBAY_START", 1))
        # end = int(os.getenv("EBAY_END", 10))
        links = LinkExtractor(
            tags="a",
            attrs="href",
            restrict_xpaths="//div/a[@class='b-visualnav__tile b-visualnav__tile__default']"
        ).extract_links(response)
        for data in links:
            name = data.text.lower().split(" ")
            try:
                brand = await Brand.objects.aget(name__lower__in=name)
            except Brand.DoesNotExist or Brand.MultipleObjectsReturned:
                brand = await Brand.objects.aget(name="No brand")

            kwargs["brand"] = brand
            yield Request(
                url=data.url,
                cb_kwargs=kwargs,
                callback=self.parse_brands_products
            )

    async def parse_brands_products(self, response, **kwargs):
        products = response.xpath(
            "//li[contains(@class, 's-item')]")
        for product in products:
            url = self.parse_url(product)
            name = self.parse_name(product)
            price = self.parse_price(product)
            condition = self.parse_condition(product)
            original_price = self.parse_original_price(product)
            image = self.parse_image(product)
            items_sold = self.parse_items_sold(product)
            shipping = self.parse_shipping_charges(product)
            ratings = self.parse_ratings(product)

            item = ProductsItem()
            item["name"] = name
            item["description"] = ""
            item["brand"] = kwargs["brand"]
            item["url"] = url
            item["price"] = item.get_price(price)
            item["by"] = Product.By.EBAY
            item["images"] = image
            item["original_price"] = original_price
            item["items_sold"] = items_sold
            item["shipping_charges"] = item.get_shipping_charges(shipping)
            item["ratings"] = ratings
            item["discount"] = item.calc_discount(price, original_price)
            item["condition"] = item.get_condition(condition)
            item["category"] = await item.get_category(kwargs["category"], kwargs["sub_category"])
            yield item

    def parse_name(self, product):
        return product.xpath(".//img[@class='s-item__image-img']/@alt").get()

    def parse_url(self, product):
        return product.xpath(".//a[@class='s-item__link']/@href").get()

    def parse_price(self, product):
        price = product.xpath(".//span[@class='s-item__price']/text()").extract()
        price = list(map(lambda x: re.sub(r"[^\d.]", "", x), price))
        return sorted(price, key=lambda x:float(x))

    def parse_original_price(self, product):
        original_price = product.xpath(".//span[@class='STRIKETHROUGH']/text()").get()
        if original_price:
            if re.search(r"\d", original_price):
                return re.sub(r"[^\d.]", "", original_price)
        return 0

    def parse_image(self, product):
        image = product.xpath(".//img[@class='s-item__image-img']")[0].attrib
        try:
            image = image["data-src"]
        except KeyError:
            image = image["src"]
        return [image]

    def parse_items_sold(self, product):
        items_sold = product.xpath(".//span[@class='s-item__hotness s-item__itemHotness']/text()").get()
        if items_sold:
            if "was" in items_sold.lower():
                return items_sold
        return 0

    def parse_shipping_charges(self, product):
        return product.xpath(".//span[@class='s-item__shipping s-item__logisticsCost']/text()").get()

    def parse_ratings(self, product):
        return 0

    def parse_condition(self, product):
        return product.xpath(".//span[@class='SECONDARY_INFO']/text()").get()
