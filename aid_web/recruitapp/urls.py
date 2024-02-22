from django.urls import path

from .views import RecruitAPIView

urlpatterns = [path("recruit_info", RecruitAPIView.as_view())]
