from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):  # 회원가입
        password = validated_data.pop("password", None)

        if password is not None:
            user = User.objects.create(
                email=validated_data["email"],
                nick_name=validated_data["nick_name"],
            )
            user.set_password(password)
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def check_user(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("user not found")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nick_name"]
