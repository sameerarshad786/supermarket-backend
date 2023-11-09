import re
import json
import aiohttp
import asyncio

from decimal import Decimal

from lxml import html

from products.models import Review, Store
from products.pipelines import ProductsPipeline, ReviewsPipeline, StoresPipeline


class DarazProductDetailSpider:
    name = "product-details"

    def __init__(self, product, **kwargs):
        self.product = product

    async def start_request(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await self.parse(response)

    async def parse(self, response, **kwargs):
        page = html.fromstring(await response.text(), "lxml")
        script_content = page.xpath("//script/text()")
        instance = self.product

        for line in script_content:
            match = re.search(r'app\.run\(({.*?})\);', line)

            if match:
                json_data = match.group(1)
                data = json.loads(json_data)
                data = data["data"]["root"]["fields"]
                tasks = [
                    self.update_product(data, instance),
                    self.insert_or_update_reviews(data, instance),
                    self.insert_or_update_store(data, instance)
                ]
                await asyncio.gather(*tasks)

    async def update_product(self, data, instance):
        product_options = data["productOption"]["options"]
        images = list(map(lambda x: x["image"], product_options))
        product = {}
        _product = data["product"]
        html_desc = _product["desc"].replace("\"", "'")
        ratings = data["review"]["ratings"]["average"]
        product["ratings"] = Decimal(ratings)
        product["html"] = html_desc
        from products.service import union
        product["images"] = union(instance.images, images)
        product["description"] = _product["highlights"]
        product["url"] = instance.url

        try:
            last_object = list(data["specifications"].keys())[-1]
            product["meta"] = data["specifications"][last_object]

        except KeyError:
            product["meta"] = dict()

        await ProductsPipeline.process_item(
            ProductsPipeline,
            product,
            "product-details"
        )

    async def insert_or_update_reviews(self, data, product):
        reviews = data["review"]["reviews"]
        reviews_list = []
        for value in reviews:
            review = dict()
            review["name"] = value["reviewer"]
            review["source"] = Review.Source.SCRAPED
            review["review"] = value.get("reviewContent", "")
            review["rating"] = Decimal(value["rating"])
            if value.get("images"):
                images = list(map(lambda x: x["url"], value["images"]))
                review["images"] = images
            reviews_list.append(review)

        await ReviewsPipeline.process_item(reviews_list, product)

    async def insert_or_update_store(self, data, instance):
        store = dict()
        store["name"] = data["seller"]["name"]
        store["by"] = Store.By.DARAZ
        try:
            store["url"] = "https:{}".format(data["seller"]["url"])
        except KeyError:
            store["url"] = ""
        store["category_id"] = instance.category_id

        await StoresPipeline.process_item(store, instance)
