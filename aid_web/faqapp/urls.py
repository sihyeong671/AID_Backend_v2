from django.urls import path

from .views import FAQAPIView, FAQListAPIView

urlpatterns = [
    path("faq/", FAQListAPIView.as_view()),
    path("faq/", FAQAPIView.as_view()),
]
