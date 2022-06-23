from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from utils.timestamps import Timestamp


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('must have user username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, Timestamp):
    objects = UserManager()  # custom user 생성 시 필요

    username = models.CharField("사용자 계정", max_length=20, unique=True)
    email = models.EmailField("이메일 주소", max_length=100)
    password = models.CharField("비밀번호", max_length=128)
    phone = models.CharField("연락처", max_length=15)

    is_active = models.BooleanField("활성화 여부", default=True)
    is_admin = models.BooleanField("관리자 여부", default=False)
    is_staff = models.BooleanField("판매자 여부", default=False)

    # id로 사용 할 필드 지정.
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user"
