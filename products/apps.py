from django.apps import AppConfig
from django.db.models.functions import Lower, Upper
from django.contrib.postgres.fields import DecimalRangeField
from django.db.models import CharField


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self) -> None:
        import products.signals
        CharField.register_lookup(Lower)
        DecimalRangeField.register_lookup(Lower)
        DecimalRangeField.register_lookup(Upper)
