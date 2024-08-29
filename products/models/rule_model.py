from django.db import models

from utils.mixins import UUID


class Rule(UUID):
    """
    Rule model is for the rules that use to extract the data from the
    crawled pages.
    """
    field_name = models.CharField(max_length=255)
    is_navigation = models.BooleanField(default=False)
    product_scraper = models.ForeignKey("products.ProductScraper", on_delete=models.CASCADE)
