from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from product.models import Cart
from product.serializer import CartSerializer

from datetime import datetime

from utils.permissions import IsBuyer


# 본인 장바구니
class CartListCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, ordered=False)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 본인 장바구니 품목 상세 정보
class CartDetailAPI(APIView):
    permission_classes = [IsBuyer]

    def _get_object(self, id):
        cart = get_object_or_404(Cart, id=id)
        return cart

    def get(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cart = self._get_object(id)
        cart.is_active = False
        cart.deleted_at = datetime.now()
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
