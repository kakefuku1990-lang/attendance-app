import calendar
from datetime import date, timedelta

from django.utils import timezone

from attendance.models import AttendanceRecord
from attendance.models import LeaveRequest


class AttendanceService:

    @staticmethod
    def get_monthly_attendance(user, year=None, month=None):

        today = timezone.localdate()

        year = int(year) if year else today.year
        month = int(month) if month else today.month

        _, last_day = calendar.monthrange(year, month)

        records = AttendanceRecord.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )

        leaves = LeaveRequest.objects.filter(
            user=user,
            date__year=year,
            date__month=month,
            status="approved"
        )

        record_map = {r.date.day: r for r in records}
        leave_map = {l.date.day: l for l in leaves}

        days = []
        total_work = timedelta()
        total_overtime = timedelta()

        for day in range(1, last_day + 1):

            record = record_map.get(day)
            leave = leave_map.get(day)

            work = record.work_duration() if record else timedelta()
            overtime = record.overtime_duration() if record else timedelta()

            total_work += work
            total_overtime += overtime

            days.append({
                "date": date(year, month, day),
                "record": record,
                "leave": leave,
                "work": work,
                "overtime": overtime,
            })

        return {
            "days": days,
            "total_work": total_work,
            "total_overtime": total_overtime,
            "year": year,
            "month": month,
        }