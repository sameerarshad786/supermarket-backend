from django.db import models

from users.models import User
from utils.mixins import UUID
from .product_model import Product


class CartItem(UUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Cart(UUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_item = models.ManyToManyField(CartItem, blank=True)
