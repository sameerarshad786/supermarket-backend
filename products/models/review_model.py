from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.mixins import UUID
from users.models import User
from products.models import Product


class Review(UUID):
    class Stars(models.TextChoices):
        ONE_STAR = ("1", _("1 Star"))
        TWO_STARS = ("2", _("2 Stars"))
        THREE_STARS = ("3", _("3 Stars"))
        FOUR_STARS = ("4", _("4 Stars"))
        FIVE_STARS = ("5", _("5 Stars"))

    class Sources(models.TextChoices):
        SCRAPED = ("scraped", _("Scraped"))
        CURRENT = ("current", _("Current"))

    name = models.CharField(max_length=50)
    review = models.TextField()
    star = models.CharField(choices=Stars.choices)
    source = models.CharField(choices=Sources.choices)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
