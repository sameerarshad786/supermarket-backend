import re
import json
import aiohttp
import asyncio

from decimal import Decimal

from lxml import html

from products.models import Product
from products.pipelines import ProductsPipeline, ReviewsPipeline, StoresPipeline
from products.items import ProductsItem


class EbayProductDetailSpider:
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
            match = re.search(r'concat\(({.*?})\)', line)
            if match:
                start = line.find("concat({") + 7
                end = line.find("});")
                json_data = line[start:end]
                data = json.loads(json_data)
                data = data["o"]["w"][0][2]["model"]["modules"]
                tasks = [
                    self.update_product(data, instance),
                    self.insert_or_update_reviews(data, instance),
                    self.insert_or_update_store(data, instance)
                ]
                await asyncio.gather(*tasks)

    async def update_product(self, data, instance: Product):
        details = data["JSONLD"]
        pictures = data["PICTURE"]["mediaList"]
        images = list(map(lambda x: x["image"]["originalImg"]["URL"], pictures))
        price = [details["product"]["offers"]["price"]]
        product = dict()
        from products.service import union
        product["images"] = union(instance.images, images)
        try:
            brand = details["product"]["brand"]["name"]
            product["brand"] = await ProductsItem.get_brand(ProductsItem, brand)
        except KeyError:
            pass
        product["url"] = instance.url
        product["price"] = ProductsItem.get_price(ProductsItem, price)
        try:
            product["shipping"] = Decimal(details["product"]["offers"]["shippingDetails"]["shippingRate"]["value"])
        except KeyError:
            pass
        try:
            product["rating"] = Decimal(data["REVIEWS"]["starRating"]["averageRating"]["value"])
        except KeyError:
            pass
        await ProductsPipeline.process_item(
            ProductsPipeline,
            product,
            "product-details"
        )

    async def insert_or_update_reviews(self, data, product):
        try:
            reviews = data["FEEDBACK_DETAIL_LIST_TABBED_V2"]["feedbackTabViews"][0]["feedbackCards"]
            reviews_list = []
            for value in reviews:
                review = dict()
                review["review"] = value["feedbackInfo"]["comment"]["accessibilityText"]
                data = value["feedbackInfo"]["context"]["textSpans"][0]["text"].split(" ")
                review["name"] = data[0]
                reviews_list.append(review)

            await ReviewsPipeline.process_item(reviews_list, product)
        except KeyError:
            pass

    async def insert_or_update_store(self, data, instance):
        data = data["STORE_INFORMATION"]
        store = dict()
        try:
            store["name"] = data["title"]["action"]["params"]["store_name"]
        except:
            store["name"] = data["title"]["action"]["params"]["_ssn"]
        store["by"] = Product.By.EBAY
        store["url"] = data["title"]["action"]["URL"]
        if not "H9YAAOSwrR1g05VS" in data["sections"][0]["logo"]["URL"]:
            store["main_photo"] = data["sections"][0]["logo"]["URL"]
        store["category_id"] = instance.category_id

        await StoresPipeline.process_item(store, instance)
