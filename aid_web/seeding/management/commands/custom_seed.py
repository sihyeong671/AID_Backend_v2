from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from userapp.models import User


# 예시: python manage.py seed_users --superuser=1 --user=10 --study=5
class Command(BaseCommand):
    help = "랜덤한 유저 데이터 생성을 이 커맨드를 활용해 할 수 있음"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--superuser", default=0, type=int, help="몇 명의 슈퍼_유저 데이터를 만드나.")
        parser.add_argument("--user", default=0, type=int, help="몇 명의 유저 데이터를 만드나.")
        parser.add_argument("--study", default=0, type=int, help="몇 개의 스터디 데이터를 만드나.")

    def handle(self, *args: Any, **options: Any) -> str | None:
        superuser = options.get("superuser")
        user = options.get("user")
        options.get("study")

        # 한국 지역에 적용되는 값을 가져옴
        # faker docs Link: https://faker.readthedocs.io/en/master/locales/ko_KR.html
        seeder = Seed.seeder(locale="ko_KR")

        # superuser 데이터를 만들 때는
        seeder.add_entity(
            User,
            superuser,
            {
                "nick_name": lambda x: seeder.faker.unique.name_female(),
                "email": lambda x: seeder.faker.unique.email(),
                "password": lambda x: seeder.faker.msisdn(),
                "is_admin": lambda x: True,
            },
        )
        # create super user

        seeder.add_entity(
            User,
            user,
            {
                "nick_name": lambda x: seeder.faker.unique.name_male(),
                "email": lambda x: seeder.faker.unique.email(),
                "password": lambda x: seeder.faker.msisdn(),
                "is_admin": lambda x: False,
            },
        )
        # Django Seed 활용하여 FK 포함한 모델의 test data 생성하기
        # Link: https://ninefloor-design.tistory.com/323
        # seeder.add_entity(
        #     Study,
        #     study,
        #     {
        #         "study_name": lambda x: seeder.faker.bs(),
        #         "study_description": lambda x: seeder.faker.catch_phrase(),
        #         "study_link": lambda x: seeder.faker.url(),
        #         "status": lambda x: randint(0, 2),
        #     },
        # )
        seeder.execute()
