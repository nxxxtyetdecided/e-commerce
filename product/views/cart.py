from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from product.models import Cart
from product.serializer import CartSerializer
<<<<<<< HEAD

from datetime import datetime

from utils.permissions import IsBuyer


# 본인 장바구니
class CartListCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, ordered=False)
=======
from utils.permissions import IsOwner


class CartListCreateAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        cart = Cart.objects.filter(buy=False)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
<<<<<<< HEAD
        serializer = CartSerializer(data=request.data, context={'user': request.user})
=======
        serializer = CartSerializer(data=request.data)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


<<<<<<< HEAD
# 본인 장바구니 품목 상세 정보
class CartDetailAPI(APIView):
    permission_classes = [IsBuyer]
=======
class CartDetailAPI(APIView):
    permission_classes = [IsOwner]
>>>>>>> c26191a53523a55a676f700082773a543ef514bd

    def _get_object(self, id):
        cart = get_object_or_404(Cart, id=id)
        return cart

    def get(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart)
<<<<<<< HEAD
        return Response(serializer.data, status=status.HTTP_200_OK)
=======
        return Response(serializer.data)
>>>>>>> c26191a53523a55a676f700082773a543ef514bd

    def put(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cart = self._get_object(id)
<<<<<<< HEAD
        cart.is_active = False
        cart.deleted_at = datetime.now()
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
=======
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateAPI(APIView):
    def get(self):
        pass

    def post(self):
        pass


class OrderDetailAPI(APIView):
    def get(self):
        pass
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
