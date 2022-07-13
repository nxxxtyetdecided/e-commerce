from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import SignUpAPI, LoginAPI

urlpatterns = [
        path('signup', SignUpAPI.as_view()),
        path('login', LoginAPI.as_view()),

        # JWT
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]