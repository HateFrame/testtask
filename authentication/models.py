from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .utils import *
import jwt
from datetime import datetime, timedelta


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None,
                    **extra_fields
                    ):

        if username is None:
            raise TypeError('User should have a username')
        if email is None:
            raise TypeError('User should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):

        if password is None:
            raise TypeError('User password should not be none')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, default='No Name')
    last_name = models.CharField(max_length=255, default='No Last Name')
    image = models.ImageField(
        upload_to=content_file_name,
        max_length=512,
        blank=True,
        default=''
    )

    class GenderChoices(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    gender = models.CharField(max_length=127, choices=GenderChoices.choices, default=GenderChoices.MALE)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save()
        if not self.image:
            return
        add_watermark(self.image)

