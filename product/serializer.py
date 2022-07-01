from rest_framework import serializers

from product.models import Category, Product, ProductOption


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        exclude = ('id',)


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('product', 'name', 'price',)


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    seller = serializers.SerializerMethodField()
    product_option = ProductOptionSerializer(many=True)

    def get_seller(self, obj):  # serializerMethodField
        return obj.seller.username

    def create(self, validated_data):
        product_option = validated_data.pop("product_option")

        product = Product(**validated_data)
        product.seller = self.context['request'].user
        product.save()

        ProductOption.objects.create(product=product, **product_option)
        return product

    class Meta:
        model = Product
        fields = ("seller", "title", "thumnail", "category", "description", "product_option", "is_active")
