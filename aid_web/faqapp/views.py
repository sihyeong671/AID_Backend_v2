from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FAQ
from .serializers import FQASerializers


class FAQAPIView(APIView):
    permission_classes = [AllowAny]  # 커스텀 권한 만들기

    @extend_schema(
        summary="FAQ POST API",
        description="FAQ 관련 데이터 생성",
    )
    def post(self, request):
        serializer = FQASerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, faq_id):
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()
        return Response("delete success", status=status.HTTP_204_NO_CONTENT)


class FAQListAPIView(APIView):
    permission_classes = [AllowAny]  # 커스텀 권한 만들기

    @extend_schema(
        summary="FAQ GET API",
        description="FAQ 관련 데이터 전달",
    )
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FQASerializers(faqs, many=True)
        res = Response(serializer.data, status=status.HTTP_200_OK)
        return res
