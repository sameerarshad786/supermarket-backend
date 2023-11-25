from rest_framework import serializers

from products.models import Category, Brand, Product, Store, Cart
from .serializer_fields import DecimalRangeFieldSerializer
from .review_serializer import ReviewSerializer


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "sub_category")

    def create(self, validated_data):
        name = validated_data.get("name").capitalize()
        return Category.objects.create(name=name)

    def get_sub_category(self, obj):
        return obj.sub_category.name if obj.sub_category else None


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    on_cart = serializers.SerializerMethodField()
    by = serializers.CharField(default=Product.By.NOT_DEFINED)
    brand = BrandSerializer()
    category = CategorySerializer(required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "images",
            "price",
            "ratings",
            "condition",
            "url",
            "category",
            "discount",
            "brand",
            "by",
            "on_cart"
        ]

    def get_on_cart(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.cart.cart_item.filter(product_id=obj.id).exists()
        else:
            return False

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        store = Store.objects.get(id=validated_data["store"])
        store.product.add(product)
        return product


class ProductDataSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    reload = serializers.HyperlinkedIdentityField(
        view_name="reload",
        lookup_field="id"
    )
    reviews = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    brand = BrandSerializer()

    class Meta:
        model = Product
        exclude = (
            "is_active",
            "is_deleted"
        )

    def get_fields(self):
        request = self.context["request"]
        fields = super().get_fields()
        if request.method == "POST":
            fields.update({
                "source": serializers.CharField(default=Product.Source.CURRENT),
                "store": serializers.UUIDField(),
                "images": serializers.ListField(
                    child=serializers.FileField(required=False), required=False
                )
            })
        return fields

    def get_reviews(self, obj):
        return ReviewSerializer(
            obj.review_set.all(),
            context={**self.context},
            many=True
        ).data

    def get_store(self, obj):
        if obj.store_set.exists():
            from products.serializers import StoreSerializer
            return StoreSerializer(
                obj.store_set.get(),
                context={**self.context},
            ).data
        return {}
