from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


User = get_user_model()

# 打刻履歴モデル
class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    # class Meta:
    #     unique_together = ("user", "date")
    #     ordering = ["-date"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_date"
            )
        ]

    def __str__(self):
        return f"{self.user.username} {self.date}"

class Department(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 社員情報モデル
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.ForeignKey(
        Department,
        null=True,
        on_delete=models.PROTECT
    )
    def __str__(self):
        return f"{self.user.username} profile"

