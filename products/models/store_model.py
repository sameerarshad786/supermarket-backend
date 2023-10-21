from django.db import models

from utils.mixins import UUID
from users.models import User
from .product_model import Product, Type


def store_main_photo_path(instance, filename):
    return f"store/main/{instance.id}/{filename}"


def store_cover_photo_path(instance, filename):
    return f"store/cover/{instance.id}/{filename}"


class Store(UUID):
    name = models.CharField(max_length=100)
    main_photo = models.ImageField(
        default="store/main/main.png", upload_to=store_main_photo_path
    )
    cover_photo = models.ImageField(
        default="store/cover/cover.png", upload_to=store_cover_photo_path
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ManyToManyField(Product)
