from django.utils.translation import gettext_lazy as _
from django.db import models

from utils.mixins import UUID
# from products.models import ProductScraper


class Rules(UUID):
    class RuleType(models.TextChoices):
        XPATH = "xpath", _("Xpath")
        REGEX = "regex", _("Regex")
        JSON = "json", _("Json")
        DATA = "data", _("Data")

    extractor_type = models.CharField(max_length=5, choices=RuleType.choices)
    pattern = models.CharField(max_length=200)
    field_name = models.CharField(max_length=50)
    field = models.ForeignKey("products.productscraper", on_delete=models.CASCADE)
