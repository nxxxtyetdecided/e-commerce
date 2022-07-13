from django.db import transaction
from rest_framework import serializers

<<<<<<< HEAD
from product.models import Category, Product, Cart, OrderItem, ProductOption
=======
from product.models import Category, Product, ProductOption
>>>>>>> c26191a53523a55a676f700082773a543ef514bd


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        exclude = ('id',)


class ProductOptionSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = ProductOption
        fields = ("name", "price",)
=======

    class Meta:
        model = ProductOption
        fields = ('name', 'price',)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    seller = serializers.SerializerMethodField()
<<<<<<< HEAD
    product_option = ProductOptionSerializer(many=True)
=======
    product_option = ProductOptionSerializer(many=True, required=False)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd

    def get_seller(self, obj):  # serializerMethodField
        return obj.seller.username

    @transaction.atomic
    def create(self, validated_data):
<<<<<<< HEAD
        print(validated_data)
        product_option = validated_data.pop('product_option')
=======
        product_options = validated_data.pop("product_option")
>>>>>>> c26191a53523a55a676f700082773a543ef514bd

        product = Product(**validated_data)
        product.seller = self.context['request'].user
        product.save()

<<<<<<< HEAD
        ProductOption.objects.create(product=product, **product_option)

=======
        for product_option in product_options:
            ProductOption.objects.create(product=product, **product_option)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
        return product

    class Meta:
        model = Product
<<<<<<< HEAD
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
=======
        fields = (
            "seller",
            "title",
            "thumnail",
            "category",
            "description",
            "product_option",
            "is_active"
        )


class CartSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):  # serializerMethodField
        return obj.customer.username

class OrderSerializer(serializers.ModelSerializer):
    pass
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
