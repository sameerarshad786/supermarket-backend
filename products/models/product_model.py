from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import DecimalRangeField
from django.core.validators import MaxValueValidator, MinValueValidator

from utils.mixins import UUID


def scraped_products_media_path(instance, filename):
    return f"scraped-products/{instance.id}/{filename}"


class Type(UUID):
    type = models.CharField(max_length=150, unique=True)
    valid_name = models.BooleanField(default=False)


class Product(UUID):
    class Condition(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        NEW = "new", _("New")
        USED = "used", _("Used")
        OPEN_BOX = "open box", _("Open Box")
        REFURBISHED = "refurbished", _("Refurbished")
        DEAD = "dead", _("Dead")

    class By(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        AMAZON = "amazon", _("Amazon")
        EBAY = "ebay", _("Ebay")
        DARAZ = "daraz", _("Daraz")
        ALI_EXPRESS = "ali express", _("Ali Express")
        ALI_BABA = "ali baba", _("Ali Baba")
        OLX = "olx", _("olx")

    class Source(models.TextChoices):
        SCRAPED = ("scraped", _("Scraped"))
        CURRENT = ("current", _("Current"))

    class Brand(models.TextChoices):
        NOT_DEFINED = "not defined", _("Not Defined")
        APPLE = "apple", _("Apple")
        SAMSUNG = "samsung", _("Samsung")
        GOOGLE = "google", _("Google")
        LG = "lg", _("LG")
        HUAWEI = "huawei", _("Huawei")
        HTC = "htc", _("HTC")
        ONEPLUS = "oneplus", _("OnePlus")
        BLACKBERRY = "blackberry", _("BlackBerry")
        MOTOROLA = "motorola", _("Motorola")
        NOKIA = "nokia", _("Nokia")
        REDMI = "redmi", _("Redmi")
        OPPO = "oppo", _("Oppo")
        VIVO = "vivo", _("Vivo")
        ITEL = "itel", _("Itel")
        INFINIX = "infinix", _("Infinix")
        SONY = "sony", _("Sony")
        REALME = "realme", _("Realme")
        TECHNO = "tecno", _("Tecno")
        XIAOMI = "xiaomi", _("Xiaomi")
        HONOR = "honor", _("Honor")

    name = models.CharField(max_length=500)
    description = models.TextField()
    brand = models.CharField(
        max_length=11, choices=Brand.choices, default=Condition.NOT_DEFINED)
    type = models.ForeignKey(
        Type, on_delete=models.SET_NULL, blank=True, null=True)
    images = ArrayField(models.CharField(max_length=200), default=list)
    url = models.URLField(unique=True, max_length=500)
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
        obj = ProductDocument(
            meta={"id": self.id},
            id=self.id,
            name=self.name,
            images=self.images,
            price=price,
            brand=self.brand,
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
