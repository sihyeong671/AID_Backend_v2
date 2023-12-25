from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=45)
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
