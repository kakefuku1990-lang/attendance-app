from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime, time, timedelta
from django.utils import timezone

User = get_user_model()

# 打刻履歴モデル
class AttendanceRecord(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()

    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    break_minutes = models.IntegerField(default=60)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_date"
            )
        ]
    # 休憩計算ロジック
    def work_duration(self):

        if not self.clock_in or not self.clock_out:
            return None

        work = self.clock_out - self.clock_in

        break_time = timedelta(minutes=self.break_minutes)

        return work - break_time

    # 残業時間自動算出メソッド
    def overtime_duration(self):

        if not self.clock_out:
            return timedelta()

        # 基準時刻（18:00）
        base_time = datetime.combine(self.date, time(18, 0))
        # タイムゾーン定義
        base_time = timezone.make_aware(base_time)

        # clock_out が18:00より前なら残業なし
        if self.clock_out <= base_time:
            return timedelta()

        return self.clock_out - base_time

    def __str__(self):
        return f"{self.user.username} {self.date}"

class Department(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 社員情報モデル
class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    department = models.ForeignKey(
        Department,
        null=True,
        on_delete=models.PROTECT
    )

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="subordinates"
    )

    def __str__(self):
        return f"{self.user.username} profile"


# 申請テーブル
class AttendanceCorrectionRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "申請中"),
        ("approved", "承認"),
        ("rejected", "却下"),
    ]

    user = models.ForeignKey(
        # User,
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    requested_clock_in = models.DateTimeField(
        null=True,
        blank=True
    )

    requested_clock_out = models.DateTimeField(
        null=True,
        blank=True
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.user} {self.date} 修正申請"


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.status == "approved":

            record, created = AttendanceRecord.objects.get_or_create(
                user=self.user,
                date=self.date
            )

            if self.requested_clock_in:
                record.clock_in = self.requested_clock_in

            if self.requested_clock_out:
                record.clock_out = self.requested_clock_out

            record.save()


# 休暇申請テーブル
class LeaveRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "申請中"),
        ("approved", "承認"),
        ("rejected", "却下"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"],
                name="unique_user_leave_date"
            )
        ]

    def __str__(self):
        return f"{self.user} {self.date} 休暇申請"


# 残業申請ロジック
class OvertimeRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "申請中"),
        ("approved", "承認"),
        ("rejected", "却下"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    hours = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    reason = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.date} 残業申請"

