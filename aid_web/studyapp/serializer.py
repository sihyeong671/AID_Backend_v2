from typing import Any

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from userapp.models import User

from .models import Study, StudyUserRelation

# from .docs import study_extend_schema_serializer

# https://www.django-rest-framework.org/api-guide/relations/

# CRUD별로 다른 serializer를 써야할 때
# https://velog.io/@haremeat/Django-%ED%95%98%EB%82%98%EC%9D%98-APIView%EC%97%90%EC%84%9C-Serializerclass%EA%B0%80-%EB%8B%A4%EB%A5%BC-%EB%95%8C
# https://github.com/encode/django-rest-framework/issues/1563


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nick_name", "email")


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            "스터디 내 사용자 정보",
            summary="스터디 내 사용자 정보",
            value={
                "study_name": "study1",
                "user_email": "testname@example.com",
                "user_id": 1,
                "is_approve": True,
            },
            request_only=False,
            response_only=True,
        )
    ],
)
class StudyUserSerializer(serializers.Serializer):
    study_name = serializers.CharField(source="study.study_name")
    user_email = serializers.CharField(source="user.email")
    user_id = serializers.IntegerField(source="user.id")
    is_approve = serializers.BooleanField()

    class Meta:
        model = StudyUserRelation
        fields = ("study_name", "user_email", "user_id", "is_approve")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "스터디 정보",
            summary="스터디 정보",
            description="스터디 정보 출력",
            value={
                "id": 1,
                "status_readable": "Opened",
                "leader": {"id": 1, "nick_name": "testname1", "email": "testname1@example.com"},
                "users": [
                    {"study_name": "study1", "user_email": "testname1@example.com", "user_id": 1, "is_approve": True}
                ],
                "study_name": "study1",
                "study_description": "testdescription1",
                "study_link": None,
                "status": 0,
                "img_url": "test",
                "created_at": "2024-01-01T00:00:00.000000Z",
            },
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            "스터디 생성",
            summary="스터디 생성",
            description="스터디 생성 및 수정용 response body",
            value={
                "study_name": "test study name",
                "study_description": "test study description",
                "status": 0,
                "study_url": "http://test.study.url/",
                "img_url": "testimg.jpg",
            },
            request_only=True,
            response_only=False,
        ),
        OpenApiExample(
            "스터디 수정",
            summary="스터디 수정 summary",
            description="스터디 수정 description",
            value={
                "study_name": "modified study name",
                "study_description": "modified study description",
                "status": 1,
                "study_url": "http://modified.study.url/",
                "img_url": "modifiedimg.jpg",
            },
            request_only=True,
            response_only=False,
        ),
    ]
)
class StudySerializer(serializers.ModelSerializer):
    status_readable = serializers.ChoiceField(
        source="get_status_display", choices=Study.StatusType.choices, read_only=True
    )
    leader = UserSerializer(many=False, read_only=True)
    users = StudyUserSerializer(many=True, read_only=True, source="studyuserrelation_set")
    # users_waiting = UserSerializer(many=True, read_only=True)

    def create(self, validated_data: dict[str, Any]) -> Study:
        leader = validated_data["leader"]
        instance = Study.objects.create(**validated_data)

        studyuserrelation_set = [StudyUserRelation(user_id=leader.id, study_id=instance.id, is_approve=True)]
        instance.studyuserrelation_set.add(*studyuserrelation_set, bulk=False)

        return instance

    class Meta:
        model = Study
        fields = "__all__"
