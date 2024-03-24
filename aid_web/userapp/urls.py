from django.urls import path

from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, UserView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
]
