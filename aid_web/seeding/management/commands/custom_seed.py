from random import randint
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django_seed import Seed
from projectapp.models import Project
from studyapp.models import Study
from userapp.models import User


# 예시: python manage.py seed_users --superuser=1 --user=10 --study=5
class Command(BaseCommand):
    help = "you can use this command for making random user data"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--superuser", default=0, type=int, help="생성할 슈퍼 유저 수")
        parser.add_argument("--user", default=0, type=int, help="생성할 유저 수")
        parser.add_argument("--study", default=0, type=int, help="생성할 스터디 수")
        parser.add_argument("--project", default=0, type=int, help="생성할 프로젝트 수")

    def handle(self, *args: Any, **options: Any):
        options.get("superuser")
        user = options.get("user")
        study = options.get("study")
        project = options.get("project")
        # 한국 지역에 적용되는 값을 가져옴
        # faker docs Link: https://faker.readthedocs.io/en/master/locales/ko_KR.html
        seeder = Seed.seeder(locale="ko_KR")

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

        seeder.add_entity(
            Study,
            study,
            {
                "study_name": lambda x: seeder.faker.unique.bs(),
                "study_description": lambda x: seeder.faker.catch_phrase(),
                "study_link": lambda x: seeder.faker.url(),
                "status": lambda x: randint(0, 2),
                "img_url": lambda x: seeder.faker.image_url(),
            },
        )

        seeder.add_entity(
            Project,
            project,
            {
                "project_name": lambda x: seeder.faker.unique.bs(),
                "project_description": lambda x: seeder.faker.catch_phrase(),
                "project_link": lambda x: seeder.faker.url(),
                "status": lambda x: randint(0, 2),
                "img_url": lambda x: seeder.faker.image_url(),
            },
        )

        seeder.execute()
