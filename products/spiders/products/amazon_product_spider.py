import re
import scrapy

from decimal import Decimal

from lxml import html
from scrapy.http import Request

from products.items import ProductsItem
from products.models import Product


class AmazonProductSpider(scrapy.Spider):
    name = Product.By.AMAZON
    domain = "https://www.amazon.com"

    custom_settings = {
        "ITEM_PIPELINES": {
            "products.pipelines.ProductsPipeline": 100
        }
    }

    def start_requests(self):
        yield Request(
            url=self.domain, meta={"playwright": True}
        )

    def parse(self, response, **kwargs):
        electronics_section = response.xpath(
            "//div/div[contains(div/h2, 'Electronics')]/a"
        ).attrib.get("href")
        yield Request(
            url=f"{response.request.url}{electronics_section}",
            callback=self.parse_electronic
        )

    def parse_electronic(self, response, **kwargs):
        page = html.fromstring(response.text, "lxml")
        all_results = page.xpath("//a[@class='a-link-normal']")[0].get("href")
        full_url = f"{self.domain}{all_results}"
        yield Request(
            url=full_url,
            callback=self.parse_products,
            meta={"next": full_url}
        )

    # def crawl_pages(self, response, **kwargs):
    #     page_numbers = response.xpath("//ol[@class='pagination__items']/li[last()]/a/text()") # noqa

    #     for page in range(1, page_numbers+1):
    #         current_url = response.request.url
    #         if current_url.endswith("/"):
    #             url = f"{response.request.url}?_pgn={page}"
    #         else:
    #             url = f"{response.request.url}&_pgn={page}"
    #         yield Request(url=url, callback=self.parse_products)

    async def parse_products(self, response, **kwargs):
        page = html.fromstring(response.text, "lxml")
        products = page.xpath("//div[@class='a-section a-spacing-base']")

        for product in products:
            url = f"{self.domain}{self.parse_url(product)}"
            name = self.parse_name(product)
            price = self.parse_price(product)
            original_price = self.parse_original_price(product, price)
            items_sold = self.parse_items_sold(product)
            image = self.parse_image(product)
            ratings = self.parse_ratings(product)
            shipping_charges = 0

            item = ProductsItem()
            item["name"] = name
            item["description"] = ""
            item["brand"] = Product.Brand.NOT_DEFINED
            item["url"] = url
            item["price"] = item.get_price(price)
            item["by"] = Product.By.AMAZON
            item["items_sold"] = items_sold
            item["shipping_charges"] = shipping_charges
            item["original_price"] = original_price
            item["images"] = [image]
            item["condition"] = Product.Condition.NOT_DEFINED
            item["ratings"] = item.get_ratings(ratings)
            item["discount"] = item.calc_discount(price, original_price)
            item["type"] = await item.get_type("Electronics")
            yield item

        if next := page.xpath("//a[contains(text(), 'Next')]/@href")[0]:
            full_url = f"{self.domain}{next}"
            yield Request(
                url=full_url,
                callback=self.parse_products,
                meta={"next": full_url, "Referer": response.request.url},
                cb_kwargs=kwargs
            )

    def parse_name(self, product):
        if name := product.xpath(".//img[@class='s-image']/@alt"):
            return name[0]
        elif name := product.xpath(".//a/div/h2/span/text()"):
            return name[0]
        else:
            return ""

    def parse_image(self, product):
        if image := product.xpath(".//img[@class='s-image']/@src"):
            return image[0]
        else:
            return ""

    def parse_url(self, product):
        url = product.xpath(".//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style']/@href") # noqa
        return url[0] if url else ""

    def parse_price(self, product):
        price_list = product.xpath(".//span[@class='a-offscreen']/text()")
        try:
            valid_price =  list(map(lambda x: re.sub(r"[^\d.]", "", x), price_list)) # noqa
        except Exception:
            price_list = product.xpath(".//span[@class='a-offscreen']/text()")
            price_exception = [price.extract() for price in price_list]
            valid_price =  list(map(lambda x: re.sub(r"[^\d.]", "", x), price_exception)) # noqa
        return sorted(valid_price)

    def parse_original_price(self, product, price):
        original_price = product.xpath(
            ".//span[@class='a-price a-text-price']/span/text()"
        )
        if original_price:
            valid_price =  list(map(lambda x: re.sub(r"[^\d.]", "", x), original_price)) # noqa
            return Decimal(valid_price[0]) + Decimal(price[0])
        return 0

    def parse_items_sold(self, product):
        if item_sold := product.xpath(
            "//span[@class='a-size-mini a-color-secondary']/text()"
        ):
            sold = item_sold[0].split(" ")[0]
            if "k" in sold.lower():
                total = sold.replace("k+", "000").replace("K+", "000")
            elif "m" in sold.lower():
                total = sold.replace("m+", "000000").replace("M+", "000000")
            return total
        return 0

    def parse_ratings(self, product):
        return product.xpath(
            ".//span/span[@class='a-size-mini puis-normal-weight-text']/text()"
        )
