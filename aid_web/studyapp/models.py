from django.db import models
from django.db.models import Model
from userapp.models import User

# class StudyManager():
#     def create_study(self, study_name, study_description, study_link,
#                      status, leader, users, img_url, created_at):


class Study(Model):
    study_name = models.CharField(max_length=50)
    study_description = models.CharField(max_length=300)
    study_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField()
    leader = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="leader")
    users = models.ManyToManyField(User)  # realted name
    img_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.study_name

    class Meta:
        db_table = "Study"
