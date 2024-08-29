from django.db import models


from utils.mixins import UUID
from products.constants import By
# from products.models import "products.Extractor"


class StartUl(UUID):
    url = models.URLField()
    name = models.ForeignKey("products.ProductScraper", on_delete=models.CASCADE)
