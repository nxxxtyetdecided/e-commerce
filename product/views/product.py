from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.utils import timezone

from product.models import Category, Product
from product.serializer import CategorySerializer, ProductSerializer
from utils.permissions import IsAdminOrReadOnly, IsStaffOrReadOnly


class CategoryListCreateAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def _get_object(self, id):
        category = get_object_or_404(Category, id=id)
        return category

    def get(self, request, id):
        category = self._get_object(id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = self._get_object(id)
        serializer = CategorySerializer(category, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self._get_object(id)
        category.is_active = False
        category.deleted_at = timezone.now()
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPI(APIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPI(APIView):
    def _get_object(self, id):
        product = get_object_or_404(Product, id=id)
        return product

    def get(self, request, id):
        product = self._get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        product = self._get_object(id)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self._get_object(id)
        product.is_active = False
        product.deleted_at = timezone.now()
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)