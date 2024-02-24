from django.db import models
from django.db.models import IntegerChoices, Model


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
    max_participants = models.PositiveIntegerField(default=0)
    leader = models.CharField(max_length=50, null=True)
    img_url = models.ImageField(upload_to="study_image/", default=None)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.study_name

    class Meta:
        db_table = "Study"
        get_latest_by = ("status", "created_at")
