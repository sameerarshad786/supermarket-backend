# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import colorama

from dotenv import load_dotenv

from products.models import Product

load_dotenv()


class ProductsPipeline:

    async def process_item(self, item, spider):
        try:
            product = await Product.objects.aget(url=item.get("url"))
            print(item, colorama.Fore.YELLOW)
        except Product.DoesNotExist:
            product = Product(**item)
            print(item, colorama.Fore.GREEN)
        await product.asave()
