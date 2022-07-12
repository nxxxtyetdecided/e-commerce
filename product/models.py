from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import User
from utils.timestamps import ActiveTime


class Category(ActiveTime):
    name = models.CharField("카테고리명", max_length=10)

    class Meta:
        db_table = "category"


class Product(ActiveTime):
    title = models.CharField("제품명", max_length=30)
    thumnail = models.ImageField("썸네일", upload_to="product/thumbnail", \
                                 height_field=None, width_field=None, max_length=None, null=True)
    description = models.TextField("설명")
    seller = models.ForeignKey(User, verbose_name="판매자", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "product"


class ProductOption(ActiveTime):
    product = models.ForeignKey(Product, verbose_name="상품명", related_name="product_option", on_delete=models.CASCADE)
    name = models.CharField("옵션명", max_length=15)
    price = models.IntegerField("가격")

    class Meta:
        db_table = "product_option"


class Cart(models.Model):
    customer = models.ForeignKey(User, verbose_name="고객", on_delete=models.CASCADE)
    product_option = models.ForeignKey(ProductOption, verbose_name="상품명(조건)", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField("수량")
    buy = models.BooleanField("구매 여부", default=False)

    def price(self):
        return self.quantity * self.product_option.price

    class Meta:
        db_table = "cart"


class Order(models.Model):
    customer = models.ForeignKey(User, verbose_name="고객", on_delete=models.CASCADE)
    order_date = models.DateField("구매 일자", auto_now_add=True)
    transaction_id = models.DateTimeField("주문번호")

    class ShippingStatus(models.TextChoices):
        PAY_COMPLETE = "PAY_COMPLETE", _("결제 완료")
        PREPARING = "PREPARING", _("배송 준비중")
        SHIPPING = "SHIPPING", _("배송중")
        DELIVER = "DELIVER", _("배송 완료")

    status = models.CharField(
        max_length=15,
        choices=ShippingStatus.choices,
        default=ShippingStatus.PAY_COMPLETE
    )

    def __str__(self):
        return self.transaction_id

    @property
    def get_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_price for item in orderitems])
        print(f"주문 총 가격 {total}")
        return total

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    product = models.ForeignKey(
                                ProductOption,
                                verbose_name="상품",
                                on_delete=models.SET_NULL,
                                null=True
                                )
    quantity = models.PositiveSmallIntegerField("수량")

    @property
    def get_price(self):
        price = self.product.price * self.quantity
        return price

    class Meta:
        db_table = "order_item"


