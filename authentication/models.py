from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .utils import *


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    image='',
                    gender='M',
                    password=None,
                    first_name='No Name',
                    last_name='No Last Name',
                    ):

        if username is None:
            raise TypeError('User should have a username')
        if email is None:
            raise TypeError('User should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            image=image,
            gender=gender
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, first_name='Admin', last_name='Admin'):

        if password is None:
            raise TypeError('User password should not be none')

        user = self.create_user(username, email, password, first_name, last_name)
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

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=127, choices=GENDER_CHOICES, default=GENDER_CHOICES[0][0])

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
