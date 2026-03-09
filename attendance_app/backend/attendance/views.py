from django.shortcuts import render

# Create your views here.
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import AttendanceRecord

# 当日打刻画面
@login_required
def punch_view(request):
    today = date.today()

    record, created = AttendanceRecord.objects.get_or_create(
        user=request.user,
        date=today,
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "clock_in" and record.clock_in is None:
            record.clock_in = timezone.now()
            record.save()

        elif action == "clock_out" and record.clock_out is None:
            record.clock_out = timezone.now()
            record.save()

        return redirect("punch")

    return render(request, "attendance/punch.html", {"record": record})

# 勤怠一覧画面
@login_required
def attendance_list(request):
    records = AttendanceRecord.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "attendance/list.html",
        {"records": records}
    )