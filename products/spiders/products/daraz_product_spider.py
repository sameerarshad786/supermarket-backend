import os
import json
import scrapy

from decimal import Decimal

from scrapy.http import Request

from products.items import ProductsItem
from products.models import Product


class DarazProductSpider(scrapy.Spider):
    name = Product.By.DARAZ
    headers_file = open("products/headers/daraz.json")
    headers = json.loads(headers_file.read())


    def start_requests(self):
        yield Request(
            url="https://www.daraz.pk/",
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        for data in response.xpath("//li[@class='lzd-site-menu-sub-item']"):
            if data.xpath('./a/span/text()').get() in [os.getenv("DARAZ_SUB_CATEGORIES")]:
                url = f"https:{data.xpath('./a/@href').get()}"
                self.headers["Referer"] = response.request.url
                yield Request(
                    url=url,
                    headers=self.headers,
                    callback=self.crawl_pages
                )

    def crawl_pages(self, response, **kwargs):
        start = int(os.getenv("DARAZ_START", 2))
        end = int(os.getenv("DARAZ_END", 10))

        for page in range(start, end + 1):
            url = f"{response.request.url}?page={page}"
            self.headers["Referer"] = response.request.url
            yield Request(
                url=url,
                headers=self.headers,
                callback=self.parse_product_brands
            )

    async def parse_product_brands(self, response, **kwargs):
        json_values = response.xpath(
            "//script[contains(text(), 'window.pageData')]"
        ).get().replace("</script>", "")
        try:
            try_dump_data = json.loads(json_values.split("=", 1)[1])
        except json.JSONDecodeError:
            pass

        products = try_dump_data["mods"]["listItems"]
        for product in products:
            url = "https:" + product["productUrl"]
            name = product["name"]
            description = product["description"][0] if product.get("description") else "" # noqa
            brand = product["brandName"]
            price = [Decimal(os.getenv("PKR_TO_DOLLAR")) * Decimal(product["price"])] # noqa
            original_price = self.parse_original_price(product, price[0])
            image = product["image"]
            items_sold = 0
            ratings = Decimal(product["ratingScore"]) if product.get("ratingScore") else 0 # noqa
            shipping = self.calc_shipping(product.get("shipping_charges"))
            discount = int(product["discount"].replace("%", "")) if product.get("discount") else 0 # noqa

            item = ProductsItem()
            item["name"] = name
            item["description"] = description
            item["brand"] = await item.get_brand(brand)
            item["url"] = url
            item["price"] = item.get_price(price)
            item["by"] = Product.By.DARAZ
            item["images"] = [image]
            item["original_price"] = original_price
            item["items_sold"] = items_sold
            item["shipping_charges"] = shipping
            item["ratings"] = ratings
            item["discount"] = discount
            item["condition"] = Product.Condition.NOT_DEFINED
            item["category"] = await item.get_category(os.getenv("DARAZ_SUB_CATEGORIES"))
            yield item

    def parse_original_price(self, product, price):
        try:
            original_price = Decimal(os.getenv("PKR_TO_DOLLAR")) * int(product["originalPrice"]) # noqa
        except Exception:
            original_price = price
        return original_price

    def calc_shipping(self, shipping):
        if shipping:
            return Decimal(os.getenv("PKR_TO_DOLLAR")) * int(shipping)
        else:
            return 0.00
