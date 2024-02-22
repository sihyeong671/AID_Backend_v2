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
            data = {"ko": {"title": "지원 기간이 아닙니다"}, "en": {"title": "It's not a application period"}}
            return Response({"data": data}, status=status.HTTP_200_OK)

        data = {
            "ko": {
                "title": "신입 부원 모집",
                "recruitment_schedule": "24.2.26 ~ 24.3.8",
                "num_of_people_recruited": "10 ~ 20명",
                "recruitment_target": "인공지능에 관심있이 있고 주도적으로 공부할 사람",
                "recruitment_link": "https://forms.gle/k4NcvS7VG8PUhe927",
                "OT_schedule": "03.15",
                "announcement_schedule": "03.09",
            },
            "en": {
                "title": "Recruiting new club members",
                "recruitment_schedule": "24.2 ~ 24.3",
                "num_of_people_recruited": "10 ~ 20",
                "recruitment_target": "People who are interested in AI and want to take the lead in studying it",
                "recruitment_link": "https://forms.gle/k4NcvS7VG8PUhe927",
                "OT_schedule": "03.15",
                "announcement_schedule": "03.09",
            },
        }

        res = Response({"data": data}, status=status.HTTP_200_OK)

        return res
