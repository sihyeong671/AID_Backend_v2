from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Study


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

    class Meta:
        model = Study
        fields = "__all__"
