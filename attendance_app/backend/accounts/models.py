from django.db import models
from django.contrib.auth.models import AbstractUser


# カスタムUSER
class User(AbstractUser):

    ROLE_CHOICES = [
        ("employee", "社員"),
        ("manager", "上長"),
        ("admin", "管理者"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="employee"
    )

# Create your models here.
