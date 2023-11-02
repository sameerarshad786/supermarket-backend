import re
import json
import scrapy

from decimal import Decimal
from scrapy.http import Request

from products.items import ProductDetailItem
from products.models import Product, Review
from products.utils import union


class DarazProductDetail(scrapy.Spider):
    name = "product-details"

    custom_settings = {
        'ITEM_PIPELINES': {
            'products.pipelines.ProductDetailPipline': 200
        }
    }

    def __init__(self, product, product_id, url, **kwargs):
        self.product = Product(product)
        self.product_id = product_id
        self.url = url

    def start_requests(self, **kwargs):
        yield Request(
            url=self.url,
            callback=self.parse,
            cb_kwargs=kwargs
        )

    async def parse(self, response, **kwargs):
        script_content = response.css('script::text').getall()

        instance = await Product.objects.aget(id=self.product_id)

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
                    yield product_detail

                except json.decoder.JSONDecodeError as e:
                    print(e)
