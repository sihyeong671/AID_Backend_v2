from django.urls import include, path
from rest_framework import routers

from .views import LoginView, UserViewset

router = routers.DefaultRouter()
router.register("user", UserViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
]
