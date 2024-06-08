from rest_framework import serializers

from products.models import ProductQuestion


class ProductQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestion
        fields = ("id", "name", "user", "product", "question", "answer")
