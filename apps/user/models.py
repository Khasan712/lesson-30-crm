from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .enums import UserRole


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=9, choices=UserRole.choices(), blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)

    def __str__(self):
        return self.phone

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]
