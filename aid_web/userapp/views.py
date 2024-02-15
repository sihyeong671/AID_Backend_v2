from django.contrib.auth import login, logout
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterAPIView(APIView):
    # https://velog.io/@kjyeon1101/DRF-JWT-%EC%9D%B8%EC%A6%9D%EC%9D%84-%EC%82%AC%EC%9A%A9%ED%95%9C-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EB%A1%9C%EA%B7%B8%EC%9D%B8#2-%EC%BB%A4%EC%8A%A4%ED%85%80%EC%9C%A0%EC%A0%80-abstractbaseuser
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        summary="회원가입 API",
        description="유저 회원가입",
        examples=[
            OpenApiExample(
                name="test user 1", value={"email": "test@test.com", "nick_name": "testuser1", "password": "test1"}
            )
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
        request=LoginSerializer,
        summary="로그인 API",
        description="유저 로그인",
        examples=[OpenApiExample(name="test user 1", value={"email": "test@test.com", "password": "test1"})],
    )
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(validated_data=data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    @extend_schema(
        summary="로그아웃 API",
        description="유저 로그아웃",
    )
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


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
