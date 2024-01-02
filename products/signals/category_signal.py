from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Category, Product
from products.documents import ProductDocument


@receiver(post_save, sender=Category)
def update_product_category_from_es(sender, instance, **kwargs):
    if instance.valid_name is False:
        products = Product.objects.filter(
            category=instance, category__sub_category=instance.sub_category
        )
        category = {
            "id": instance.id,
            "category": instance.name,
            "sub_category": instance.sub_category.name
        }
        for product in products:
            product_document = ProductDocument.get(
                index=ProductDocument.index, id=product.id
            )
            product_document.update(category=category)
