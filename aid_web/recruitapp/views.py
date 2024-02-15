from datetime import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class RecruitAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="모집 일정 관련 GET API",
        description="모집 관련 데이터 전달",
    )
    def get(self, request):
        start_date = datetime(2024, 2, 22, 0, 0, 0)
        cur_date = datetime.now()
        end_date = datetime(2024, 3, 8, 23, 59, 59)

        if cur_date >= end_date or start_date >= cur_date:
            data = {"title": "지원 기간이 아닙니다"}
            return Response({"data": data}, status=status.HTTP_200_OK)

        data = {
            "title": "신입 부원 모집",
            "recruitment_schedule": "24.2 ~ 24.3",
            "num_of_people_recruited": "0명",
            "recruitment_target": "인공지능에 관심있는 사람",
            "recruitment_link": "링크 미정",
            "interview_schedule": "일정 미정",
            "OT_schedule": "일정 미정",
            "announcement_schedule": "일정 미정",
        }

        res = Response({"data": data}, status=status.HTTP_200_OK)

        return res
