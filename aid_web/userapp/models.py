from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
# https://hckcksrl.medium.com/django-%EC%BB%A4%EC%8A%A4%ED%85%80-%EC%9C%A0%EC%A0%80-%EB%AA%A8%EB%8D%B8-custom-user-model-b8487c0d150
class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        user = self.model(email=self.normalize_email(email), nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email, nickname, password)
        user.is_admin = True

        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nick_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["nick_name"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "User"
