from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import AuthAPIView, SingupAPIView

urlpatterns = [
    path("signup/", SingupAPIView.as_view()),
    path("auth/", AuthAPIView.as_view(), name="auth"),
    path("auth/refresh", TokenRefreshView.as_view()),
]
