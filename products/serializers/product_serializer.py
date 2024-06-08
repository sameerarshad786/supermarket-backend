from rest_framework import serializers

from products.models import Category, Brand, Product, Store
from .serializer_fields import DecimalRangeFieldSerializer
from .review_serializer import ReviewSerializer
from .product_question_serializer import ProductQuestionSerializer


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "sub_category")

    def create(self, validated_data):
        name = validated_data.get("name").capitalize()
        return Category.objects.create(name=name)

    def get_sub_category(self, obj):
        try:
            sub_category = obj.sub_category.name
        except:
            sub_category = obj.sub_category
        return sub_category


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    price = DecimalRangeFieldSerializer()
    on_cart = serializers.SerializerMethodField()
    by = serializers.CharField(default=Product.By.SUPERMARKET)
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
    question_answer = serializers.SerializerMethodField()

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
                "store": serializers.UUIDField(),
                "images": serializers.ListField(
                    child=serializers.FileField(required=False),
                    required=False
                )
            })
        return fields

    def get_reviews(self, obj):
        return ReviewSerializer(
            obj.review_set.all(),
            context=self.context,
            many=True
        ).data

    def get_store(self, obj):
        if obj.store_set.exists():
            from products.serializers import StoreSerializer
            return StoreSerializer(
                obj.store_set.get(),
                context=self.context,
            ).data
        return {}

    def get_question_answer(self, obj):
        return ProductQuestionSerializer(
            obj.productquestion_set.all(),
            many=True,
            context=self.context
        ).data
