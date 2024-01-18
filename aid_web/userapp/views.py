from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from .permissions import UserPermission
from .serializers import LoginSerializer, UserSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        UserPermission,
    ]


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serilaizer = self.get_serializer(data=request.data)
        serilaizer.is_valid(raise_exception=True)
        token = serilaizer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)
