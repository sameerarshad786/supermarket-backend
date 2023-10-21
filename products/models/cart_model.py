from django.db import models

from users.models import User
from utils.mixins import UUID
from .product_model import Products


class CartItem(UUID):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Cart(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_item = models.ManyToManyField(CartItem)
