# Generated by Django 4.2.6 on 2023-10-13 18:58

import uuid
from decimal import Decimal
import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from products.documents import ProductDocument


def create_products(apps, schema_editor):
    ProductDocument.build_index()


def delete_products(apps, schema_editor):
    ProductDocument.drop_index()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTypes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=150, unique=True)),
                ('valid_name', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('brand', models.CharField(choices=[('not defined', 'Not Defined'), ('apple', 'Apple'), ('samsung', 'Samsung'), ('google', 'Google'), ('lg', 'LG'), ('huawei', 'Huawei'), ('htc', 'HTC'), ('oneplus', 'OnePlus'), ('blackberry', 'BlackBerry'), ('motorola', 'Motorola'), ('nokia', 'Nokia'), ('redmi', 'Redmi'), ('oppo', 'Oppo'), ('vivo', 'Vivo'), ('itel', 'Itel'), ('infinix', 'Infinix'), ('sony', 'Sony'), ('realme', 'Realme'), ('tecno', 'Tecno'), ('xiaomi', 'Xiaomi'), ('honor', 'Honor')], default='not defined', max_length=11)),
                ('image', models.URLField()),
                ('url', models.URLField(max_length=500, unique=True)),
                ('items_sold', models.PositiveIntegerField(default=0)),
                ('ratings', models.PositiveIntegerField(default=0)),
                ('condition', models.CharField(choices=[('not defined', 'Not Defined'), ('new', 'New'), ('used', 'Used'), ('open box', 'Open Box'), ('refurbished', 'Refurbished'), ('dead', 'Dead')], default='not defined', max_length=11)),
                ('original_price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('price', django.contrib.postgres.fields.ranges.DecimalRangeField(default=(Decimal('0.00'), Decimal('0.00')))),
                ('shipping_charges', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('source', models.CharField(choices=[('not defined', 'Not Defined'), ('amazon', 'Amazon'), ('ebay', 'Ebay'), ('daraz', 'Daraz'), ('ali express', 'Ali Express'), ('ali baba', 'Ali Baba'), ('olx', 'olx')], max_length=11)),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-100), django.core.validators.MaxValueValidator(0)])),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.producttypes')),
                ('available', models.BooleanField(default=True)),
                ('meta', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(create_products, reverse_code=delete_products)
    ]
