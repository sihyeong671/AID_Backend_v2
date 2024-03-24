from django.urls import path

from .views import NewsAPIView

# router = routers.DefaultRouter()
# router.register("news/", NewsViewSet, basename="news/")

urlpatterns = [path("news/", NewsAPIView.as_view())]
