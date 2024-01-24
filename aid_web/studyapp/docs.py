# flake8: noqa
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view

from .serializer import StudySerializer, StudyUserSerializer

study_extend_schema_view = extend_schema_view(
    list=extend_schema(tags=["스터디 CRUD"], description="스터디 목록 확인.\n\n로그인하지 않은 사용자도 확인 가능.", responses=StudySerializer),
    retrieve=extend_schema(
        tags=["스터디 CRUD"],
        description="스터디 상세정보 확인.",
        responses=StudySerializer,
        request=StudySerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="확인할 스터디 id", required=True
            )
        ],
    ),
    create=extend_schema(
        tags=["스터디 CRUD"],
        description="스터디 생성.\n\n스터디 이름, 상태는 필수로 입력. 설명, 이미지 url, 스터디 링크는 선택적으로 입력 가능.  \n스터디 상태는 0-`Opened`, 1-`Closed`, 2-`Finished`를 의미.",
        responses=StudySerializer,
        request=StudySerializer,
    ),
    update=extend_schema(
        tags=["스터디 CRUD"],
        description="스터디 수정",
        responses={
            200: OpenApiResponse(response=StudySerializer, description="스터디 수정 성공"),
            403: OpenApiResponse(description="스터디 수정 권한이 없음"),
            404: OpenApiResponse(description="스터디가 존재하지 않음"),
        },
        request=StudySerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="수정할 스터디 id", required=True
            )
        ],
    ),
    destroy=extend_schema(
        tags=["스터디 CRUD"],
        description="스터디 삭제",
        responses={
            204: OpenApiResponse(description="스터디 삭제 성공"),
            403: OpenApiResponse(description="스터디 삭제 권한이 없음"),
            404: OpenApiResponse(description="스터디가 존재하지 않음"),
        },
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="삭제할 스터디 id", required=True
            )
        ],
    ),
    quit=extend_schema(
        tags=["스터디 나가기"],
        description="스터디 나가기.\n\nAPI호출 대상이 되는 스터디에 현재 로그인 한 사용자가 있다면, 스터디를 나감. 스터디 leader라면 leader를 None으로 변경.",
        request=None,
        responses={
            200: OpenApiResponse(response=StudySerializer, description="스터디 나가기 성공"),
        },
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="나갈 스터디 id", required=True
            )
        ],
    ),
    join=extend_schema(
        tags=["스터디 참가, 승인"],
        description="스터디 참가.\n\n현재 로그인 된 사용자 이름으로 스터디 참가 신청.",
        request=None,
        responses={
            200: OpenApiResponse(response=StudySerializer, description="스터디 참가 성공"),
            403: OpenApiResponse(description="이미 스터디에 참가함, 스터디가 Opened 상태가 아님."),
        },
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="참가할 스터디 id", required=True
            )
        ],
    ),
    approval=extend_schema(
        tags=["스터디 참가, 승인"],
        description="스터디 참가 승인을 위해 스터디 참가자 목록 확인.\n\n스터디에 참가중인 사용자와, 참가 신청한 사용자가 함께 표시되고, 승인되지 않은 사용자는 `is_approve`가 `false`로 표시.",
        request=None,
        responses=StudyUserSerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="참가자 목록을 확인할 스터디 id", required=True
            )
        ],
    ),
    approval_with_id=extend_schema(
        tags=["스터디 참가, 승인"],
        description="스터디 참가 승인.\n\n스터디 leader나 admin만 가능.",
        request=None,
        responses={
            200: OpenApiResponse(response=StudyUserSerializer, description="참가 승인 성공"),
            404: OpenApiResponse(description="스터디 또는 참가자가 존재하지 않음"),
        },
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="참가자를 승인할 스터디 id", required=True
            ),
            OpenApiParameter(
                name="user_id", type=int, location=OpenApiParameter.PATH, description="참가 승인할 사용자 id", required=True
            ),
        ],
    ),
    reject_with_id=extend_schema(
        tags=["스터디 참가, 승인"],
        description="참가자 삭제.\n\nleader가 자기 자신을 삭제하거나, admin이 leader를 삭제하는 것은 불가능. leader를 다른 사람에게 넘겨줘야 가능함.  \n로그인 된 사용자가 자기 자신을 스터디에서 삭제하려면 `quit` API를 사용.",
        request=None,
        responses={
            200: OpenApiResponse(response=StudySerializer, description="참가자 삭제 성공"),
            403: OpenApiResponse(description="스터디 leader를 삭제하려고 시도함."),
        },
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="참가자를 삭제할 스터디 id", required=True
            ),
            OpenApiParameter(
                name="user_id", type=int, location=OpenApiParameter.PATH, description="삭제할 사용자 id", required=True
            ),
        ],
    ),
    set_leader_with_id=extend_schema(
        tags=["스터디 리더 변경"],
        description="스터디 리더 변경.",
        request=None,
        responses=StudySerializer,
        parameters=[
            OpenApiParameter(
                name="id", type=int, location=OpenApiParameter.PATH, description="리더를 변경할 스터디 id", required=True
            ),
            OpenApiParameter(
                name="user_id", type=int, location=OpenApiParameter.PATH, description="리더로 설정할 사용자 id", required=True
            ),
        ],
    ),
)
