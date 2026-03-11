from django.shortcuts import render

# Create your views here.
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import AttendanceRecord
from .forms import LeaveRequestForm
from .models import LeaveRequest

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

# 休暇申請処理
@login_required
def leave_request_create(request):

    if request.method == "POST":

        form = LeaveRequestForm(
            request.POST,
            user=request.user
        )
        
        if form.is_valid():

            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()

            # return redirect("/"/)
            return redirect("attendance:leave_request_list")

    else:
        form = LeaveRequestForm(user=request.user)

    return render(
        request,
        "attendance/leave_request.html",
        {"form": form}
    )


# 申請履歴表示処理
@login_required
def leave_request_list(request):

    leave_requests = LeaveRequest.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "attendance/leave_request_list.html",
        {"leave_requests": leave_requests}
    )