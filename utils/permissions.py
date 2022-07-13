from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrReadOnly(BasePermission):
    """
        관리자는 모두 가능, 로그인한 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET',)

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)

        # 로그인 & 조회
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        # 로그인 & 관리자 권한 -> 생성, 수정, 삭제 가능
        return user.is_authenticated and user.is_admin


class IsStaffOrReadOnly(BasePermission):
    """
        판매자는 모두 가능, 로그인한 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET',)

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)

        # 로그인 & 조회
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        # 로그인 & 관리자 권한 -> 생성, 수정, 삭제 가능
        return user.is_authenticated and user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


<<<<<<< HEAD
class IsBuyer(BasePermission):
=======
class IsOwner(permissions.BasePermission):
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
    SAFE_METHODS = ('GET',)

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)

        # 로그인 & 조회
<<<<<<< HEAD
        if user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
=======
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user
>>>>>>> c26191a53523a55a676f700082773a543ef514bd
