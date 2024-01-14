from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):  # 회원가입
        user = User.objects.create(
            email=validated_data["email"],
            nick_name=validated_data["nick_name"],
        )
        user.set_password(validated_data["password"])
        Token.objects.create(user=user)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError({"error": "Unable to login"})
