from django.db import models
from django.db.models import IntegerChoices, Model
from userapp.models import User


class Study(Model):
    # https://www.b-list.org/weblog/2007/nov/02/handle-choices-right-way/
    class StatusType(IntegerChoices):
        OPENED = 0
        CLOSED = 1
        FINISHED = 2

    study_name = models.CharField(max_length=50, unique=True)
    study_description = models.CharField(max_length=300, blank=True)
    study_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField(choices=StatusType.choices, default=StatusType.OPENED)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leader")
    users = models.ManyToManyField(User, through="StudyUserRelation")  # realted name
    # users_waiting = models.ManyToManyField(User, blank=True, related_name="users_waiting")
    img_url = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.study_name

    class Meta:
        db_table = "Study"
        get_latest_by = ("status", "created_at")


class StudyUserRelation(models.Model):
    # 스터디 참여 여부 및 확장성을 위한 중간 테이블 명시.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    is_approve = models.BooleanField(default=False)

    class Meta:
        db_table = "study_user"
