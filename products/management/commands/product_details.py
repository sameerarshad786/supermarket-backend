from django.core.management.base import BaseCommand

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from products import settings as my_settings
from products.spiders.details import DarazProductDetail


class Command(BaseCommand):
    help = 'Scraping product details'

    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        runner = CrawlerProcess(settings=crawler_settings)
        runner.crawl(DarazProductDetail)
        runner.start()
