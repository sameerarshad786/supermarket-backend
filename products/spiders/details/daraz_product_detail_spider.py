import re
import json
import scrapy

from decimal import Decimal

from scrapy.http import Request

from products.items import ProductDetailItem
from products.models import Product, Review


class DarazProductDetail(scrapy.Spider):
    name = "product-details"
    start_urls = ["https://www.daraz.com"]

    async def parse(self, response, **kwargs):
        dataz_products = Product.objects.filter(source=Product.Source.DARAZ)
        async for product in dataz_products:
            yield Request(
                url=product.url,
                callback=self.product_details,
                cb_kwargs={"product": product}
            )

    async def product_details(self, response, **kwargs):
        script_content = response.css('script::text').getall()

        instance: Product = kwargs["product"]

        for line in script_content:
            match = re.search(r'app\.run\((.*?)\);', line)
            if match:
                json_data = match.group(1)

                try:
                    data = json.loads(json_data)
                except json.decoder.JSONDecodeError:
                    json_data = json_data + ')"}}}}}'
                    data = json.loads(json_data)

                store_data = data["data"]["root"]["fields"]
                ratings = Decimal(store_data["review"]["ratings"]["average"])
                instance.ratings = ratings
                try:
                    last_object = list(store_data["specifications"].keys())[-1]
                    instance.meta = store_data["specifications"][last_object]
                except KeyError:
                    instance.meta = dict()
                await instance.asave()

                store = dict()
                store["name"] = store_data["seller"]["name"]
                store["url"] = "https:{}".format(store_data["seller"]["url"])
                store["type"] = instance.type

                review = dict()
                reviews = data["data"]["root"]["fields"]["review"]["reviews"]
                for value in reviews:
                    review["name"] = value["reviewer"]
                    review["source"] = Review.Sources.SCRAPED
                    review["review"] = value.get("reviewContent", "")
                    review["rating"] = Decimal(value["rating"])
                    try:
                        images = list(map(lambda x: x["url"], value["images"]))
                        review["images"] = images
                    except KeyError:
                        pass

                product_detail = ProductDetailItem()
                product_detail["store"] = store
                product_detail["product"] = instance
                product_detail["review"] = review
                yield product_detail
