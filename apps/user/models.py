from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from apps.user.managers import UserManager
from .enoms import UserRole

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=9, choices=UserRole.choices())
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True, editable=True, blank=True, null=True)

    def __str__(self):
        return self.phone_number
    
    
    objects = UserManager()

    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", 'role']

    

