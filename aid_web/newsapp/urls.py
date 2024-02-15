from rest_framework import routers

from .views import NewsViewSet

router = routers.DefaultRouter()
router.register("news", NewsViewSet, basename="news")

urlpatterns = router.urls
