from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from utils.mixins import UUID
from users.models import User
from products.models import Product


class ProductQuestion(UUID):
    name = models.CharField(max_length=50)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
