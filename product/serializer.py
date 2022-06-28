from rest_framework import serializers

from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    seller = serializers.SerializerMethodField()

    def get_seller(self, obj): # serializerMethodField
        return obj.seller.username

    def create(self, validated_data):
        product = Product(**validated_data)
        product.seller = self.context['request'].user
        product.save()

        return product

    class Meta:
        model = Product
        fields = ("seller", "title", "thumnail", "category", "description", "is_active")
