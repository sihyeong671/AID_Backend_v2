# Create your models here.
from django.db import models


class FAQ(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "FAQ"
