from django.urls import path

<<<<<<< HEAD
from product.views.category import CategoryListCreateAPI, CategoryDetailAPI
from product.views.product import ProductListCreateAPI, ProductDetailAPI
=======
from product.views.product import CategoryListCreateAPI, CategoryDetailAPI, \
                                    ProductListCreateAPI, ProductDetailAPI
>>>>>>> c26191a53523a55a676f700082773a543ef514bd

urlpatterns = [
    path("categories", CategoryListCreateAPI.as_view()),
    path("categories/<int:id>", CategoryDetailAPI.as_view()),
    path("products", ProductListCreateAPI.as_view()),
    path("products/<int:id>", ProductDetailAPI.as_view()),
]