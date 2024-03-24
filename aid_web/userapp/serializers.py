import uuid

from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):  # 회원가입
        password = validated_data.pop("password", None)

        # 처음 회원 가입하는 경우 nick name 자동 생성
        nick_name = f"user-{uuid.uuid1()[:10]}"

        if password is not None:
            user = User.objects.create(
                email=validated_data["email"],
                nick_name=nick_name,
            )
            user.set_password(password)
            # save
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nick_name"]
