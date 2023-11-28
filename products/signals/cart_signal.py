from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal

from products.models import Cart
from users.models import User


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    """
    create_user's cart if new user created
    """
    if created:
        Cart.objects.create(user_id=instance.id)
