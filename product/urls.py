from django.urls import path

from product.views.category import CategoryListCreateAPI, CategoryDetailAPI
from product.views.product import ProductListCreateAPI, ProductDetailAPI

urlpatterns = [
    path("categories", CategoryListCreateAPI.as_view()),
    path("categories/<int:id>", CategoryDetailAPI.as_view()),
    path("products", ProductListCreateAPI.as_view()),
    path("products/<int:id>", ProductDetailAPI.as_view()),
]