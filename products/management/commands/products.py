from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from products import settings as my_settings
from products.models import ProductScraper
from products.spiders import ProductSpider


class Command(BaseCommand):
    help = 'Scraping products'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        runner = CrawlerProcess(settings=crawler_settings)
        # runner.crawl(EbayProductsSpider)
        # runner.crawl(DarazProductSpider)
        runner.crawl(
            ProductSpider,
            scraper=ProductScraper.objects.select_related(
                "name",
                "description",
                "brand",
                "url",
                "images",
                "items_sold",
                "condition",
                "original_price",
                "shipping_charges",
                "discount",
                "available",
                "html",
                "meta"
            ).prefetch_related("next_page").first()
        )
        runner.start()
