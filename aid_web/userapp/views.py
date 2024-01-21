import jwt
from config.settings.base import SIMPLE_JWT
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User
from .serializers import UserSerializer


class SingupAPIView(APIView):
    # https://velog.io/@kjyeon1101/DRF-JWT-%EC%9D%B8%EC%A6%9D%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%9C-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EB%A1%9C%EA%B7%B8%EC%9D%B8#2-%EC%BB%A4%EC%8A%A4%ED%85%80%EC%9C%A0%EC%A0%80-abstractbaseuser
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        summary="회원가입 API",
        description="유저 회원가입",
        examples=[
            OpenApiExample(
                name="test user 1", value={"email": "test@test.com", "nick_name": "testuser1", "password": "test1"}
            )
        ],
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "sign up success",
                    "token": {"access": access_token, "refresh": refresh_token},
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # TODO
        # refresh token은 갱신시키면 안됨
        # access token만 refresh token이 존재할 때 갱신할 것
        # 위의 로직이 맞는지 확인
        try:
            access = request.COOKIES["access"]
            payload = jwt.decode(access, SIMPLE_JWT["SIGNING_KEY"], algorithms=SIMPLE_JWT["ALGORITHM"])
            pk = payload.get("user_id")
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            data = {"refresh": request.COOKIES.get("refresh", None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get("access", None)
                refresh = serializer.data.get("refresh", None)
                payload = jwt.decode(access, SIMPLE_JWT["SIGNING_KEY"], algorithms=SIMPLE_JWT["ALGORITHM"])
                pk = payload.get("user_id")
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie("access", access)
                res.set_cookie("refresh", refresh)
                return res
            raise jwt.exceptions.InvalidTokenError
        except jwt.exceptions.InvalidTokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = authenticate(email=request.data.get("email"), password=request.data.get("password"))
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh = str(token)
            access = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "log in success",
                    "token": {"access": access, "refresh": refresh},
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access", access)
            res.set_cookie("refresh", refresh)
            return res
        else:
            return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        res = Response({"message": "log out success"}, status=status.HTTP_202_ACCEPTED)
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res
