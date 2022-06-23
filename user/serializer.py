from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # password -> hash 적용
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = (
                  "username", "email", "password", "phone",
                  "is_active", "is_admin", "is_staff",
                )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }
    """
        field에 없으면 설정한 기본 값으로 들어오지만,
        입력 받은 값이 없을 시에 False로 입력됨
        is_active의 default=True -> 빈칸이면 False로 입력받음
    """
