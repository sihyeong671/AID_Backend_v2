# Create your views here.
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from userapp.models import User

from .models import Study, StudyUserRelation
from .permissions import IsOwnerOfStudyOrAdmin
from .serializer import StudySerializer, StudyUserSerializer


# TODO: queryset.get() 호출할 때 DoesNotExist 예외 처리
class StudyViewSet(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    # 인증되지 않은 사용자는 읽기만(GET) 가능. 수정, 삭제 등은 study leader나 관리자만 가능.
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfStudyOrAdmin]

    # 스터디 생성. serializer의 create를 override해서 중간 테이블을 포함해 저장.
    # override
    def perform_create(self, serializer):
        serializer.save(leader=self.request.user)

    # 스터디 나가기. 나가려는 사람이 leader라면 leader를 None으로 변경.
    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticatedOrReadOnly])
    @transaction.atomic()
    def quit(self, request, pk):
        instance = self.get_object()
        instance.users.remove(request.user)
        if instance.leader == request.user:
            instance.leader = None
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 스터디 참가. 스터디다 OPENED 상태여야 하고, 이미 참가한 사람은 참가 불가.
    # 참가한 사용자는 참가 여부인 is_approve가 false.
    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticatedOrReadOnly])
    def join(self, request, pk):
        instance = self.get_object()
        if instance.status != Study.StatusType.OPENED:
            return Response({"detail": "Study not available"}, status=status.HTTP_403_FORBIDDEN)
        if instance.users.filter(id=request.user.id).exists():
            return Response({"detail": "User already joined study"}, status=status.HTTP_403_FORBIDDEN)
        instance.users.add(request.user)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 스터디 참가 승인을 위한 참가자 목록 확인. 스터디 leader나 관리자만 가능.
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsOwnerOfStudyOrAdmin],
    )
    def approval(self, request, pk):
        # https://stackoverflow.com/questions/69959797/has-object-permission-not-working-for-detail-action-decorator
        study_obj = self.get_object()
        user_relation = study_obj.studyuserrelation_set
        serializer = StudyUserSerializer(user_relation, many=True)
        return Response(serializer.data)

    # 스터디 참가 승인. 스터디 leader나 관리자만 가능.
    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsOwnerOfStudyOrAdmin],
        url_path=r"approval/(?P<user_id>\d+)",
    )
    def approval_with_id(self, request, pk, user_id=None):
        try:
            study_obj = self.get_object()
            user_relation = study_obj.studyuserrelation_set.get(study_id=pk, user_id=user_id)
            user_relation.is_approve = True
            user_relation.save()
            serializer = StudyUserSerializer(user_relation)
            return Response(serializer.data)
        except StudyUserRelation.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # 참가자 삭제. 스터디 leader나 관리자만 가능.
    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsOwnerOfStudyOrAdmin],
        url_path=r"reject/(?P<user_id>\d+)",
    )
    def reject_with_id(self, request, pk, user_id=None):
        instance = self.get_object()
        if int(user_id) == instance.leader.id:
            return Response({"detail": "Cannot reject leader"}, status=403)
        instance.users.remove(user_id)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # TODO
    # 스터디 리더 변경을 아래와 같이 새로운 api endpoint로 둘 지,
    # ModelViewSet이나 Serializer의 update를 override해서 구현할 지 고민.
    @transaction.atomic()
    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsOwnerOfStudyOrAdmin],
        url_path=r"set-leader/(?P<user_id>\d+)",
    )
    def set_leader_with_id(self, request, pk, user_id):
        instance = self.get_object()
        user_queryset = instance.users.filter(id=user_id)
        # TODO : exists와 get 둘 다 SQL 호출. 효율성 있게 추후 수정해보기.
        # 참가중인 유저를 leader로 만들기.
        try:
            if user_queryset.exists():
                instance.leader = user_queryset.get()
            else:  # 참가중이지 않은 유저를 leader로 만들기. users에도 추가.
                user_obj = User.objects.get(id=user_id)
                instance.leader = user_obj
                instance.users.add(user_obj)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
