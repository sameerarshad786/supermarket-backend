import os
import json
import scrapy

from decimal import Decimal

from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from products.items import ProductsItem
from products.models import Product


class DarazProductSpider(scrapy.Spider):
    name = "product"
    start_urls = ["https://www.daraz.pk/"]

    def parse(self, response, **kwargs):
        brand_names = [condition.value for condition in Product.Brand]
        categories = LinkExtractor(
            tags="a", attrs="href", restrict_xpaths="//a[@class='catLink']"
        ).extract_links(response)

        for category in categories:
            if category.text.strip().lower().split(" ")[0] in brand_names:
                brand_index = brand_names.index(
                    category.text.strip().lower().split(" ")[0]
                )
                brand = brand_names[brand_index]
                kwargs["brand"] = brand
                yield Request(
                    url=category.url,
                    callback=self.crawl_pages,
                    cb_kwargs=kwargs
                )

    def crawl_pages(self, response, **kwargs):
        json_values = response.xpath(
            "//script[contains(text(), 'window.pageData')]"
        ).get().replace("</script>", "")
        try:
            try_dump_data = json.loads(json_values.split("=", 1)[1])
        except json.JSONDecodeError:
            pass

        page_numbers = round(int(try_dump_data["mainInfo"]["totalResults"]) / int(try_dump_data["mainInfo"]["pageSize"])) # noqa

        for page in range(1, page_numbers+1):
            current_url = response.request.url
            if current_url.endswith("/"):
                url = f"{response.request.url}?page={page}"
            else:
                url = f"{response.request.url}&page={page}"
            yield Request(
                url, callback=self.parse_product_brands, cb_kwargs=kwargs
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
            price = [Decimal(os.getenv("PKR_TO_DOLLAR")) * Decimal(product["price"])] # noqa
            original_price = self.parse_original_price(product, price[0])
            image = product["image"]
            items_sold = 0
            shipping = self.calc_shipping(product.get("shipping_charges"))
            discount = int(product["discount"].replace("%", "")) if product.get("discount") else 0 # noqa

            item = ProductsItem()
            item["name"] = name
            item["description"] = ""
            item["brand"] = kwargs["brand"]
            item["url"] = url
            item["price"] = item.get_price(price)
            item["source"] = "daraz"
            item["image"] = image
            item["original_price"] = original_price
            item["items_sold"] = items_sold
            item["shipping_charges"] = shipping
            item["ratings"] = item.get_ratings(product.get("shipping_charges"))
            item["discount"] = discount
            item["condition"] = Product.Condition.NOT_DEFINED
            item["type"] = await item.get_type("Electronics")
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
