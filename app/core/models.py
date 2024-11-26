# Database models

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    # Manager for users
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(
            using=self._db
        )  # default database to use. It's the db we defined in settings.py

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Can login to django admin

    objects = UserManager()

    USERNAME_FIELD = "email"  # Replace the default field from username to email
