from django.db import models

# Create your models here.
from user.models import User
from utils.timestamps import ActiveTime


class Category(ActiveTime):
    name = models.CharField("카테고리명", max_length=10)

    class Meta:
        db_table = "category"


class Product(ActiveTime):
    title = models.CharField("제품명", max_length=30)
    thumnail = models.ImageField("썸네일", upload_to="product/thumbnail", \
                                 height_field=None, width_field=None, max_length=None)
    description = models.TextField("설명")
    seller = models.ForeignKey(User, verbose_name="판매자", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="카테고리", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "product"


class ProductOption(ActiveTime):
    product = models.ForeignKey(Product, verbose_name="상품명", on_delete=models.CASCADE)
    name = models.CharField("옵션명", max_length=15)
    price = models.IntegerField("가격")

    class Meta:
        db_table = "product_option"



