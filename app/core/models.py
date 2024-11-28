# Database models

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


class UserManager(BaseUserManager):
    # Manager for users
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have a valid email address")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)

        user.save(
            using=self._db
        )  # default database to use. It's the db we defined in settings.py

        return user

    def create_superuser(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have a valid email address")

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Can login to django admin

    objects = UserManager()

    USERNAME_FIELD = (
        "email"  # Replace the default field from username to email
    )


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    time_minutes = models.IntegerField(default=5)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
