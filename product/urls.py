from django.urls import path

from product.views.cart import CartListCreateAPI, CartDetailAPI
from product.views.order import OrderListCreateAPI, OrderDetailAPI
from product.views.product import CategoryListCreateAPI, CategoryDetailAPI, \
                                    ProductListCreateAPI, ProductDetailAPI
from product.views.review import ReviewListCreateAPI

urlpatterns = [
    path("categories", CategoryListCreateAPI.as_view()),
    path("categories/<int:id>", CategoryDetailAPI.as_view()),

    # Product
    path("products", ProductListCreateAPI.as_view()),
    path("products/<int:id>", ProductDetailAPI.as_view()),

    # Cart
    path("cartlist", CartListCreateAPI.as_view()),
    path("cartlist/<int:id>", CartDetailAPI.as_view()),

    # Order
    path("orderlist", OrderListCreateAPI.as_view()),
    path("orderlist/<int:id>", OrderDetailAPI.as_view()),

    # Review
    path("products/<int:product_id>/reviews", ReviewListCreateAPI.as_view()),
]