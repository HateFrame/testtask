from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from authentication.utils import content_file_name, add_watermark


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, default='No Name')
    last_name = models.CharField(max_length=255, default='No Last Name')
    likes = models.ManyToManyField('self', symmetrical=False)
    image = models.ImageField(
        upload_to=content_file_name,
        max_length=512,
        blank=True,
        default=''
    )

    class GenderChoices(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'

    gender = models.CharField(
        max_length=127,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )

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
        if self.image:
            add_watermark(self.image)
