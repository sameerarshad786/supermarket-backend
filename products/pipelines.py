# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import colorama
from products.models import Product, Store, Review


class ProductsPipeline:

    async def process_item(self, item, spider):
        if (
            spider.name == Product.By.DARAZ or
            spider.name == Product.By.EBAY
        ):
            try:
                product = await Product.objects.aget(url=item.get("url"))
                print(item, colorama.Fore.YELLOW)
            except Product.DoesNotExist:
                product = Product(**item)
                print(item, colorama.Fore.GREEN)
            await product.asave()


class ProductDetailPipline:

    async def process_item(self, item, spider):
        if spider == "product-details":
            store = item.get("store")
            reviews = item.get("reviews")
            product = item.get("product")

            if store:
                store_url = store.pop("url").split("?")[0]
                try:
                    store_instance = await Store.objects.aget(url=store_url)
                    # print(store, colorama.Fore.YELLOW)
                except Store.DoesNotExist:
                    store_instance = Store(**store, url=store_url)
                    # print(store, colorama.Fore.GREEN)

                await store_instance.asave()
                await store_instance.product.aadd(product.id)

            if reviews:
                for review in reviews:
                    try:
                        review_instance = await Review.objects.aget(
                            name=review["name"],
                            product=product
                        )
                        # print(review, colorama.Fore.YELLOW)
                    except Review.DoesNotExist:
                        review_instance = Review(**review, product=product)
                        # print(review, colorama.Fore.GREEN)

                    await review_instance.asave()
