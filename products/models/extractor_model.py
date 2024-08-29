from django.db import models

from utils.mixins import UUID
from products.constants import ExtractorType


class Extractor(UUID):
    extractor_type = models.CharField(
        choices=ExtractorType.choices,
        max_length=5
    )
    pattern = models.CharField(max_length=255)
    rule = models.ForeignKey("products.Rule", on_delete=models.CASCADE)
