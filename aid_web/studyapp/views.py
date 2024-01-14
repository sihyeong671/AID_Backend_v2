# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Study
from .permissions import IsOwnerOfStudyOrAdmin
from .serializer import StudySerializer


class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfStudyOrAdmin]

    # override
    def perform_create(self, serializer):
        serializer.save(leader=self.request.user)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticatedOrReadOnly])
    def quit(self, request, pk):
        instance = self.get_object()
        instance.users.remove(request.user)
        if instance.leader == request.user:
            instance.leader = None
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticatedOrReadOnly])
    def join(self, request, pk):
        instance = self.get_object()
        if instance.status != Study.StatusType.OPENED:
            return Response({"detail": "Study not available"}, status=406)
        if instance.users.filter(id=request.user.id).exists():
            return Response({"detail": "User already joined study"}, status=403)
        # if instance.users_waiting.filter(id=request.user.id).exists():
        #     return Response({"detail": "User already exists in users_waiting"}, status=403)
        # instance.users_waiting.add(request.user)
        instance.users.add(request.user)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # @action(detail=True, methods=["patch"], permission_classes=[IsOwnerOfStudyOrAdmin])
    # def approval(self, request, pk):
    #     self.get_object()
