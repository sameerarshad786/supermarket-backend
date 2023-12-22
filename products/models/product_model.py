from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import DecimalRangeField
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.mixins import UUID


def scraped_products_media_path(instance, filename):
    return f"scraped-products/{instance.id}/{filename}"


class Category(UUID):
    name = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)
    sub_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Brand(UUID):
    name = models.CharField(max_length=100, unique=True)

    @staticmethod
    def default():
        return Brand.objects.get(name="No brand")


class Product(UUID):
    class Condition(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        NEW = "new", _("New")
        USED = "used", _("Used")
        OPEN_BOX = "open box", _("Open Box")
        REFURBISHED = "refurbished", _("Refurbished")
        DEAD = "dead", _("Dead")

    class By(models.TextChoices):
        SUPERMARKET = "supermarket", _("Supermarket")
        WISEMARKET = "wisemarket", _("Wisemarket")
        AMAZON = "amazon", _("Amazon")
        EBAY = "ebay", _("Ebay")
        DARAZ = "daraz", _("Daraz")
        ALI_EXPRESS = "ali express", _("Ali Express")
        ALI_BABA = "ali baba", _("Ali Baba")
        OLX = "olx", _("olx")

    class Source(models.TextChoices):
        SCRAPED = ("scraped", _("Scraped"))
        CURRENT = ("current", _("Current"))

    name = models.CharField(max_length=500)
    description = models.TextField()
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_DEFAULT,
        default=Brand.default
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    images = ArrayField(models.CharField(max_length=200), default=list)
    url = models.URLField(unique=True, max_length=500, null=True, blank=True)
    items_sold = models.PositiveIntegerField(default=0)
    ratings = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    condition = models.CharField(
        max_length=11,
        choices=Condition.choices,
        default=Condition.NOT_DEFINED
    )
    original_price = models.DecimalField(
        default=0, max_digits=7, decimal_places=2)
    price = DecimalRangeField(default=(Decimal('0.00'), Decimal('0.00')))
    shipping_charges = models.DecimalField(
        default=0, max_digits=5, decimal_places=2)
    by = models.CharField(max_length=11, choices=By.choices)
    source = models.CharField(choices=Source.choices, default=Source.SCRAPED)
    discount = models.IntegerField(
        validators=[MinValueValidator(-100), MaxValueValidator(0)], default=0)
    available = models.BooleanField(default=True)
    html = models.TextField()
    meta = models.JSONField(default=dict)

    def get_name(self):
        return self.name if len(self.name) < 20 else f"{self.name[:20]}..."

    def indexing(self):
        from products.documents.product_document import ProductDocument
        if self.price.upper:
            price = {
                "gt": float(self.price.lower),
                "lt": float(self.price.upper)
            }
        price = {
            "gt": float(self.price.lower)
        }
        brand = {
            "id": str(self.brand.id),
            "name": str(self.brand.name)
        }
        category = {
            "id": str(self.category_id),
            "name": str(self.category.name),
            "sub_category": str(self.category.sub_category.name) if self.category.sub_category else None # noqa
        }
        obj = ProductDocument(
            meta={"id": self.id},
            id=self.id,
            name=self.name,
            images=self.images,
            price=price,
            brand=brand,
            category=category,
            condition=self.condition,
            ratings=self.ratings,
            discount=self.discount,
            by=self.by,
            url=self.url,
            created_at=self.created_at.date(),
            updated_at=self.updated_at.date()
        )
        obj.save(index='products')
        return obj.to_dict(include_meta=True)

    def delete_product_from_elasticsearch_db(self):
        from products.documents.product_document import ProductDocument
        ProductDocument().delete(
            id=self.id,
            index="products"
        )
