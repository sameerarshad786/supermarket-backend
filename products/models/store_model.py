from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.mixins import UUID
from users.models import User
from .product_model import Product, Category


def store_main_photo_path(instance, filename):
    return f"store/main/{instance.id}/{filename}"


def store_cover_photo_path(instance, filename):
    return f"store/cover/{instance.id}/{filename}"


class Store(UUID):
    class By(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        AMAZON = "amazon", _("Amazon")
        EBAY = "ebay", _("Ebay")
        DARAZ = "daraz", _("Daraz")
        ALI_EXPRESS = "ali express", _("Ali Express")
        ALI_BABA = "ali baba", _("Ali Baba")
        OLX = "olx", _("olx")

    name = models.CharField(max_length=100)
    main_photo = models.CharField(max_length=200, default="store/main/main.png")
    cover_photo = models.CharField(max_length=200, default="store/cover/cover.png")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    by = models.CharField(max_length=11, choices=By.choices)
    product = models.ManyToManyField(Product)
    url = models.URLField(unique=True, max_length=500, null=True, blank=True)
