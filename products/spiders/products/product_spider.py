import re
import json
import scrapy

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

from products.items import ProductsItem
from products.models import ProductScraper


class ProductSpider(scrapy.Spider):
    name = "product"

    def __init__(self, scraper: ProductScraper):
        self.scraper = scraper

    def start_requests(self):
        # for scraper in self.scrapers:
        for start_url in self.scraper.start_url:
            yield Request(
                url=start_url,
                callback=self.parse
            )

    def next_requests(self, url, **kwargs):
        yield Request(
            url=url,
            callback=self.parse
        )

    def extract(self, html, pattern, extractor_type):
        func = getattr(html, extractor_type)
        data = func(pattern).getall()
        return data

    def parse(self, response, **kwargs):
        link_extractor = LinkExtractor() 
        links = link_extractor.extract_links(response)
        for x in self.scraper.next_page.all():
            for link in links:
                if re.search(x.pattern, link.url):
                    yield self.next_requests(link.url)

        item = ProductsItem()
        print(response)
        # item["name"] = self.extract(response, self.scraper.name.pattern, self.scraper.name.extractor_type)
        # item["by"] = self.scraper.by
        # item["url"] = self.extract(response, self.scraper.url.pattern, self.scraper.url.extractor_type)
        yield item
