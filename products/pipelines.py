# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import colorama

from products.models import Product, Store, Review, ProductQuestion


class ProductsPipeline:

    async def process_item(self, item, spider):
        try:
            product = await Product.objects.aget(url=item.get("url"))
            for x, y in item.items():
                setattr(product, x, y)
            print(item, colorama.Fore.YELLOW)
        except Product.DoesNotExist:
            product = Product(**item)
            print(item, colorama.Fore.GREEN)

        await product.asave()


class ReviewsPipeline:
    async def process_item(reviews, product):
        if reviews:
            for review in reviews:
                try:
                    review_instance = await Review.objects.aget(
                        name=review["name"],
                        product=product
                    )
                    for x, y in review.items():
                        setattr(review_instance, x, y)
                    print(review, colorama.Fore.YELLOW)
                except Review.DoesNotExist:
                    review_instance = Review(**review, product=product)
                    print(review, colorama.Fore.GREEN)

                await review_instance.asave()


class StoresPipeline:
    async def process_item(store, product):
        if store:
            store_url = store.pop("url").split("?")[0]
            try:
                store_instance = await Store.objects.aget(url=store_url)
                for x, y in store.items():
                    setattr(store_instance, x, y)
                print(store, colorama.Fore.YELLOW)
            except Store.DoesNotExist:
                store_instance = Store(**store, url=store_url)
                print(store, colorama.Fore.GREEN)

            await store_instance.asave()
            await store_instance.product.aadd(product.id)


class QuestionAndAnswerPipeline:
    async def process_item(qna_list, product):
        if qna_list:
            for qna in qna_list:
                try:
                    qna_instance = await ProductQuestion.objects.aget(product=product)
                    for x, y in qna.items():
                        setattr(qna_instance, x, y)
                    print(qna, colorama.Fore.YELLOW)
                except ProductQuestion.DoesNotExist:
                    qna_instance = ProductQuestion(**qna, product=product)
                    print(qna, colorama.Fore.GREEN)

                await qna_instance.asave()
