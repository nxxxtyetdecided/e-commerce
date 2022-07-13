from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404

from product.models import Cart
from product.serializer import CartSerializer
from utils.permissions import IsOwner


class CartListCreateAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        cart = Cart.objects.filter(buy=False)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPI(APIView):
    permission_classes = [IsOwner]

    def _get_object(self, id):
        cart = get_object_or_404(Cart, id=id)
        return cart

    def get(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cart = self._get_object(id)
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
