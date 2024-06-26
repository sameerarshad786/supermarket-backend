from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from products import settings as my_settings
from products.spiders import (
    EbayProductsSpider, DarazProductSpider
)


class Command(BaseCommand):
    help = 'Scraping products'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        runner = CrawlerProcess(settings=crawler_settings)
        runner.crawl(EbayProductsSpider)
        runner.crawl(DarazProductSpider)
        runner.start()
