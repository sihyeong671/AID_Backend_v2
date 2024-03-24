# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Study
from .serializer import StudySerializer


class StudyViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        study = Study.objects.all()
        serializer = StudySerializer(study, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
