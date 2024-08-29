from rest_framework import serializers

from products.models import Extractor, ProductScraper


class ExtractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extractor
        fields = ("id", "extractor_type", "pattern")


# class ProductScraperSerializer(serializers.ModelSerializer):
#     name = ExtractorSerializer()
#     description = ExtractorSerializer()
#     url = ExtractorSerializer()
#     images = ExtractorSerializer()
#     brand = ExtractorSerializer()
#     items_sold = ExtractorSerializer()
#     condition = ExtractorSerializer()
#     original_price = ExtractorSerializer()
#     shipping_charges = ExtractorSerializer()
#     discount = ExtractorSerializer()
#     available = ExtractorSerializer()
#     html = ExtractorSerializer()
#     meta = ExtractorSerializer()
#     next_page = ExtractorSerializer(many=True)

#     class Meta:
#         model = ProductScraper
#         fields = (
#             "id",
#             "start_url",
#             "next_page",
#             "name",
#             "description",
#             "url",
#             "images",
#             "brand",
#             "by",
#             "items_sold",
#             "condition",
#             "original_price",
#             "shipping_charges",
#             "discount",
#             "available",
#             "html",
#             "meta"
#         )

#     def create(self, validated_data):
#         name = validated_data.pop("name")
#         description = validated_data.pop("description")
#         url = validated_data.pop("url")
#         images = validated_data.pop("images")
#         brand = validated_data.pop("brand")
#         items_sold = validated_data.pop("items_sold")
#         condition = validated_data.pop("condition")
#         original_price = validated_data.pop("original_price")
#         shipping_charges = validated_data.pop("shipping_charges")
#         discount = validated_data.pop("discount")
#         available = validated_data.pop("available")
#         html = validated_data.pop("html")
#         meta = validated_data.pop("meta")
#         next_page = validated_data.pop("next_page")
#         _name = Extractor.objects.create(
#             **name
#         )
#         next_page_instance = []
#         for n in next_page:
#             next_page_instance.append(Extractor(**n))
#         _next_page = Extractor.objects.bulk_create(next_page_instance)

#         _description = Extractor.objects.create(
#             **description
#         )
#         _url = Extractor.objects.create(
#             **url
#         )
#         _images = Extractor.objects.create(
#             **images
#         )
#         _brand = Extractor.objects.create(
#             **brand
#         )
#         _items_sold = Extractor.objects.create(
#             **items_sold
#         )
#         _condition = Extractor.objects.create(
#             **condition
#         )
#         _original_price = Extractor.objects.create(
#             **original_price
#         )
#         _shipping_charges = Extractor.objects.create(
#             **shipping_charges
#         )
#         _discount = Extractor.objects.create(
#             **discount
#         )
#         _available = Extractor.objects.create(
#             **available
#         )
#         _html = Extractor.objects.create(
#             **html
#         )
#         _meta = Extractor.objects.create(
#             **meta
#         )
#         instance = ProductScraper.objects.create(
#             name=_name,
#             description=_description,
#             url=_url,
#             images=_images,
#             brand=_brand,
#             items_sold=_items_sold,
#             condition=_condition,
#             original_price=_original_price,
#             shipping_charges=_shipping_charges,
#             discount=_discount,
#             available=_available,
#             html=_html,
#             meta=_meta,
#             **validated_data
#         )
#         instance.next_page.add(*_next_page)
#         return instance
