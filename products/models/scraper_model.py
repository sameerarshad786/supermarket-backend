from django.db import models
from django.contrib.postgres.fields import ArrayField

from utils.mixins import UUID
from products.constants import By
# from products.models import "products.Extractor"


class ProductScraper(UUID):
    name = models.CharField(max_length=155)
    # start_url = ArrayField(
    #     models.CharField(max_length=500),
    #     default=list
    # )
    # next_page = models.ManyToManyField("products.Extractor", blank=True)
    # url = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_url"
    # )
    # name = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_name"
    # )
    # description = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_description"
    # )
    # brand = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_brand"
    # )
    # images = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_images"
    # )
    # by = models.CharField(choices=By.choices, max_length=11, unique=True)
    # items_sold = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_items_sold"
    # )
    # condition = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_condition"
    # )
    # original_price = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_original_price"
    # )
    # shipping_charges = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_shipping_charges"
    # )
    # discount = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_discount"
    # )
    # available = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_available"
    # )
    # html = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_html"
    # )
    # meta = models.ForeignKey(
    #     "products.Extractor",
    #     on_delete=models.CASCADE,
    #     related_name="product_meta"
    # )
