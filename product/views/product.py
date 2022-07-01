from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from product.models import Product, ProductOption
from product.serializer import ProductSerializer, ProductOptionSerializer
from utils.permissions import IsStaffOrReadOnly

from datetime import datetime


class ProductListCreateAPI(APIView):
    """
        product 생성, 리스트
        관리자, 판매자만 가능
    """
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
    """
            product 조회, 수정, 삭제
            관리자, 판매자만 가능
        """
    permission_classes = [IsStaffOrReadOnly]

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
        product.deleted_at = datetime.now()
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductOptionListCreateAPI(APIView):
#     permission_classes = [IsStaffOrReadOnly]
#
#     # def get(self, request):
#     #     """
#     #         get이 필요한가...?
#     #         product 조회할 때 한 번에 보면 되는 거 아닌가...?
#     #         판매자가 등록한 물건의 옵션만 보여주기...
#     #     """
#     #     product_option = ProductOption.objects.filter(is_active=True)
#     #     serializer = ProductOptionSerializer(request.data, many=True)
#     def post(self, request):
#         serializer = ProductOptionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# # class ProductOptionDetailAPI(APIView):
# #     permission_classes = [IsStaffOrReadOnly]