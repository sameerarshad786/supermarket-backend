from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from utils.mixins import UUID
from users.models import User
from products.models import Product


class Review(UUID):
    class Source(models.TextChoices):
        SCRAPED = ("scraped", _("Scraped"))
        CURRENT = ("current", _("Current"))

    name = models.CharField(max_length=50)
    review = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    source = models.CharField(choices=Source.choices, default=Source.SCRAPED)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = ArrayField(models.CharField(max_length=200), default=list)
