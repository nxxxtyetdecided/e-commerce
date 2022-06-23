from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView


# 회원가입 API
from user.serializer import UserSerializer


class SignUpAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인 API
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 맞지 않습니다."},
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "Login Success"}, status=status.HTTP_200_OK)
