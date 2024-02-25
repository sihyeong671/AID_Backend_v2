from django.urls import path

from .views import StudyViewSet

# router = routers.DefaultRouter()
# router.register("study", StudyViewSet)

urlpatterns = [
    path("study", StudyViewSet.as_view()),
]
