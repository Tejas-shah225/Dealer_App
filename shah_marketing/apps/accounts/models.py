from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        DEALER = 'DEALER', 'Dealer'
        RETAILER = 'RETAILER', 'Retailer'
        PLUMBER = 'PLUMBER', 'Plumber'
        ADMIN = 'ADMIN', 'Admin'

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RETAILER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = UserManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self) -> str:
        return f'{self.name} ({self.email})'
