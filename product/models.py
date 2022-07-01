from django.db import models

# Create your models here.
from user.models import User
from utils.timestamps import ActiveTime
from django.utils.translation import gettext_lazy as _


class Category(ActiveTime):
    name = models.CharField("카테고리명", max_length=10)

    class Meta:
        db_table = "category"


class Product(ActiveTime):
    title = models.CharField("제품명", max_length=30)
    thumnail = models.ImageField("썸네일", upload_to="product/thumbnail",
                                 height_field=None, width_field=None, max_length=None)
    description = models.TextField("설명")
    seller = models.ForeignKey(User, verbose_name="판매자", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)
    like = models.ManyToManyField(User, related_name="like")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "product"


class ProductOption(ActiveTime):
    product = models.ForeignKey(Product, verbose_name="상품명", related_name="product_option", on_delete=models.CASCADE)
    name = models.CharField("옵션명", max_length=15)
    price = models.IntegerField("가격")

    def __str__(self):
        return f'{self.product} - {self.name}'

    class Meta:
        db_table = "product_option"


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="구매자", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductOption, verbose_name="상품", related_name="product_option", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField("수량")
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity}개의 {self.product}'

    def total_price(self):
        return self.quantity * self.product.price

    class Meta:
        db_table = "cart"


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="구매자", on_delete=models.CASCADE)
    order_date = models.DateTimeField("구매 시각")
    transaction_id = models.CharField("거래 번호", max_length=100, null=True)
    is_deleted = models.BooleanField("삭제 여부", default=False)
    address = models.CharField("배송지", max_length=100)

    class PayMethod(models.TextChoices):
        CARD = 'CARD', _('카드')
        CASH = 'CASH', _('현금')

    class ShippingHistory(models.TextChoices):
        READY = 'READY', _('배송 대기')
        PROGRESS = 'PROGRESS', _('배송 진행')
        ARRIVAL = 'ARRIVAL', _('배송 도착')

    @property
    def total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.all_price for item in orderitems])

        return total

    class Meta:
        db_table = 'order'
        ordering = ['-order_date']


class OrderItem(models.Model):
    product = models.ForeignKey(ProductOption, verbose_name="상품", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name="구매 정보", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField("수량")
    created_at = models.DateTimeField("생성 날짜")

    def __str__(self):
        return f'{self.product} : {self.quantity}'

    @property
    def all_price(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'order_item'
