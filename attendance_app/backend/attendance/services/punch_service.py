from django.utils import timezone
from django.db import transaction

from attendance.models import AttendanceRecord


class PunchService:

    @staticmethod
    @transaction.atomic
    def punch_in(user):
        today = timezone.localdate()

        record, created = AttendanceRecord.objects.get_or_create(
            user=user,
            date=today
        )

        if record.clock_in:
            raise ValueError("すでに出勤済みです")

        record.clock_in = timezone.now()
        record.save()

        return record

    @staticmethod
    @transaction.atomic
    def punch_out(user):
        today = timezone.localdate()

        try:
            record = AttendanceRecord.objects.get(
                user=user,
                date=today
            )
        except AttendanceRecord.DoesNotExist:
            raise ValueError("出勤記録がありません")

        if not record.clock_in:
            raise ValueError("出勤していません")

        if record.clock_out:
            raise ValueError("すでに退勤済みです")

        record.clock_out = timezone.now()
        record.save()

        return record