from products.models import Product
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Product)
def index_post(sender, instance, **kwargs):
    instance.indexing()


@receiver(post_delete, sender=Product)
def delete_data_from_elasticsearch_db(sender, instance, **kwargs):
    instance.delete_product_from_elasticsearch_db()
