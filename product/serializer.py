from rest_framework import serializers

from product.models import Category, Product, Cart, OrderItem, ProductOption


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        exclude = ('id',)


class ProductOptionSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductOption
        fields = ("name", "price",)


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    seller = serializers.SerializerMethodField()
    product_option = ProductOptionSerializer(many=True)

    def get_seller(self, obj):  # serializerMethodField
        return obj.seller.username

    def create(self, validated_data):
        print(validated_data)
        product_option = validated_data.pop('product_option')

        product = Product(**validated_data)
        product.seller = self.context['request'].user
        product.save()

        ProductOption.objects.create(product=product, **product_option)

        return product

    class Meta:
        model = Product
        fields = ("seller",
                  "title",
                  "thumnail",
                  "category",
                  "description",
                  "product_option",
                  "is_active")




class CartSerializer(serializers.ModelSerializer):
    consumer = serializers.SerializerMethodField()

    def get_consumer(self, obj):
        return obj.user

    def create(self, validated_data):
        cart = Cart(**validated_data)
        cart.user = self.context['user']
        cart.save()

        return cart

    class Meta:
        model = Cart
        exclude = ('id',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'order', 'quantity', 'all_price')


class OrderSerializer(serializers.ModelSerializer):
    consumer = serializers.SerializerMethodField()
    order_items = OrderItemSerializer(many=True, read_only=True)

    def get_consumer(self, obj):
        return obj.user

    def create(self, validated_data):
        cart = Cart(**validated_data)
        cart.user = self.context['user']
        cart.save()

        return cart

    class Meta:
        model = Cart
        fields = ('transaction_id', 'order_date', 'order_items', 'address', 'total_price',)
