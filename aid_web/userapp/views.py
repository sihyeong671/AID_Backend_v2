from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, # 토큰 생성
#     TokenRefreshView, # 토큰 유효성 확인
#     TokenVerifyView, # refresh로 access 재발급
# )


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        summary="회원가입 API",
        description="유저 회원가입",
        examples=[
            OpenApiExample(
                name="test user 1", value={"email": "test1@test.com", "nick_name": "testuser1", "password": "test1"}
            ),
            OpenApiExample(name="test user 2", value={"email": "test2@test.com", "password": "test2"}),
        ],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                res = Response(
                    {
                        "user": serializer.data,
                        "message": "sign up success",
                    },
                    status=status.HTTP_201_CREATED,
                )
                return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        summary="로그인 API",
        description="유저 로그인",
        examples=[OpenApiExample(name="test user 1", value={"email": "test@test.com", "password": "test1"})],
    )
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"message": "아이디 또는 비밀번호가 일치하지 않습니다"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        update_last_login(None, user)

        response = Response({"message": "login success", "access_token": access_token})

        response.set_cookie("refresh_token", refresh_token, httponly=True)

        return response


class LogoutAPIView(APIView):
    @extend_schema(
        summary="로그아웃 API",
        description="유저 로그아웃",
    )
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @extend_schema(
        summary="User read",
        description="유저 정보 가져오는 API",
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
