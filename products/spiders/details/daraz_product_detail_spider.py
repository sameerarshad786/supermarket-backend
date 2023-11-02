import re
import json
import aiohttp

from decimal import Decimal

from lxml import html

from products.items import ProductDetailItem
from products.models import Review
from products.pipelines import ProductDetailPipline
# from products.service import union


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
            match = re.search(r'app\.run\((.*?)\);', line)

            if match:
                json_data = match.group(1)
                try:
                    data = json.loads(json_data)
                    data = data["data"]["root"]["fields"]

                    product_options = data["productOption"]["options"]
                    images = list(map(lambda x: x["image"], product_options))
                    product = data["product"]
                    product_detail = ProductDetailItem()
                    html_desc = product["desc"].replace("\"", "'")
                    ratings = data["review"]["ratings"]["average"]
                    instance.ratings = Decimal(ratings)
                    instance.html = html_desc
                    from products.service import union
                    instance.images = union(instance.images, images)
                    instance.description = product["highlights"]

                    try:
                        last_object = list(data["specifications"].keys())[-1]
                        instance.meta = data["specifications"][last_object]

                    except KeyError:
                        instance.meta = dict()
                    await instance.asave()
                    
                    reviews = data["review"]["reviews"]

                    review_list = []
                    for value in reviews:
                        review = dict()
                        review["name"] = value["reviewer"]
                        review["source"] = Review.Source.SCRAPED
                        review["review"] = value.get("reviewContent", "")
                        review["rating"] = Decimal(value["rating"])
                        if value.get("images"):
                            images = list(map(lambda x: x["url"], value["images"]))
                            review["images"] = images
                        review_list.append(review)

                    product_detail["reviews"] = review_list
                    store = dict()
                    store["name"] = data["seller"]["name"]
                    try:
                        store["url"] = "https:{}".format(data["seller"]["url"])
                    except KeyError:
                        store["url"] = ""
                    store["type_id"] = instance.type_id

                    product_detail["store"] = store
                    product_detail["product"] = instance
                    await ProductDetailPipline.process_item(self, product_detail, self.name)

                except json.decoder.JSONDecodeError as e:
                    print(e)
