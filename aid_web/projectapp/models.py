from django.db import models
from django.db.models import Model
from userapp.models import User


class Project(Model):
    project_name = models.CharField(max_length=50, unique=True, blank=True)
    project_description = models.CharField(max_length=300, blank=True)
    project_link = models.CharField(max_length=500, null=True)
    status = models.IntegerField(editable=True, default=0)
    users = models.ManyToManyField(User)
    img_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = "Project"
