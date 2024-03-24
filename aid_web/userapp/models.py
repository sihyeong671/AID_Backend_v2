from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    # migrations로 필요에 의해 manager를 직렬하하기 위한 옵션
    use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    nick_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["nick_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        verbose_name_plural = "User"
        ordering = ("-created_at",)
