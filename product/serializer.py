from django.db import transaction
from rest_framework import serializers
from django.utils import timezone

from product.models import Category, Product, ProductOption, \
    Cart, Order, OrderItem, Review


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Category
        exclude = ('id',)


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ('name', 'price',)


class ProductSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    seller = serializers.SerializerMethodField()
    product_option = ProductOptionSerializer(many=True, required=False)

    def get_seller(self, obj):  # serializerMethodField
        return obj.seller.username

    @transaction.atomic
    def create(self, validated_data):
        product_options = validated_data.pop("product_option")

        product = Product(**validated_data)
        product.seller = self.context['request'].user
        product.save()

        for product_option in product_options:
            ProductOption.objects.create(product=product, **product_option)
        return product

    class Meta:
        model = Product
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

    def create(self, validated_data):
        cart = Cart(**validated_data)
        cart.customer = self.context['request'].user
        cart.save()
        return cart

    class Meta:
        model = Cart
        fields = ("customer", "product_option", "quantity", "buy", "total_price")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'get_price')  # price는 model에서 함수로 선언


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    order_item = OrderItemSerializer(many=True, required=False)
    get_order_items = serializers.ListField(required=False)

    def get_customer(self, obj):  # serializerMethodField
        return obj.customer.username

    @transaction.atomic
    def create(self, validated_data):
        get_order_items = validated_data.pop("get_order_items")

        # Order 생성
        order = Order(**validated_data)
        order.transaction_id = timezone.now()
        order.customer = self.context['request'].user
        order.save()

        carts = Cart.objects.prefetch_related("product_option").all()

        """ 
            Cart에 있는 품목이면 구매 여부 -> True
            OrderItem 생성
        """
        for cart in carts:
            for item in get_order_items:
                if cart.product_option.id == item:
                    cart.buy = True
                    cart.save()
                    OrderItem.objects.create(
                        order=order,
                        product=cart.product_option,
                        quantity=cart.quantity
                    )

        return order

    class Meta:
        model = Order
        fields = (
            'customer',
            'method',
            'status',
            'order_item',  # 왜 목록에 나타나지 않음...
            'transaction_id',
            'get_order_items',
            'get_total_price'
        )


class ReviewSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):  # serializerMethodField
        return obj.customer.username

    def create(self, validated_data):
        orderitem = OrderItem.objects.select_related("review").filter()
        customer = self.context['request'].user


    class Meta:
        model = Review
        fields = "__all__"
