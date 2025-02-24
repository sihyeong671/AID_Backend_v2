from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import IntegerChoices, Model


class Study(Model):
    # https://www.b-list.org/weblog/2007/nov/02/handle-choices-right-way/
    class StatusType(IntegerChoices):
        NOT_STARTED = 0
        ONGOING = 1
        FINISHED = 2

    class StudyType(IntegerChoices):
        PROJECT = 0
        STUDY = 1
        COMPETITION = 2

    study_name = models.CharField(max_length=50, unique=True)
    study_description = models.CharField(max_length=300, blank=True)
    study_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField(choices=StatusType.choices, default=StatusType.NOT_STARTED)
    study_type = models.IntegerField(choices=StudyType.choices, default=StudyType.STUDY)
    max_participants = models.PositiveIntegerField(default=0)
    leader = models.CharField(max_length=50, null=True)
    participants = ArrayField(models.CharField(max_length=50), blank=True, null=True)
    img_url = models.ImageField(upload_to="study_image/", default=None)
    created_at = models.DateTimeField(auto_now=True)
    study_start = models.DateTimeField(null=True)
    study_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.study_name

    class Meta:
        db_table = "Study"
        get_latest_by = ("status", "study_start")
