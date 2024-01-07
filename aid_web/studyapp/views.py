# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Study
from .permissions import IsOwnerOfStudyOrReadOnly
from .serializer import StudySerializer


class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfStudyOrReadOnly]

    # override
    def perform_create(self, serializer):
        serializer.save(leader=self.request.user, users=[self.request.user])

    # Q. ModelViewSet에 있는 update 사용 시 leader, users에 대한 정보를 넘기는 게 가능한가?
