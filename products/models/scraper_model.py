from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db import models

from utils.mixins import UUID


class ProductScraper(UUID):
    scraper = models.CharField(max_length=100)
    start_urls = ArrayField(models.CharField(max_length=100), default=list)
    name = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_name", null=True, blank=True)
    description = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_description", null=True, blank=True)
    images = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_images", null=True, blank=True)
    ratings = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_ratings", null=True, blank=True)
    condition = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_condition", null=True, blank=True)
    original_price = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_original_price", null=True, blank=True)
    price = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_price", null=True, blank=True)
    shipping_charges = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_shipping_charges", null=True, blank=True)
    by = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_by", null=True, blank=True)
    discount = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_discount", null=True, blank=True)
    available = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_available", null=True, blank=True)
    html = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_html", null=True, blank=True)
    meta = models.ForeignKey('products.rules', on_delete=models.CASCADE, related_name="scraper_meta", null=True, blank=True)
