from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Review
from product.serializer import ReviewSerializer
from utils.permissions import IsCustomer


class ReviewListCreateAPI(GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "product_id"

    def get(self, request):
        print(f'kwag : {self.kwargs}')
        review = Review.objects.filter(buy=False, customer=request.user)
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)