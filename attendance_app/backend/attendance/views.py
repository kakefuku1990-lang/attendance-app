from django.shortcuts import render

# Create your views here.
from datetime import date
import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import AttendanceRecord
from .forms import LeaveRequestForm
from .models import LeaveRequest
from .forms import OvertimeRequestForm
from .models import OvertimeRequest
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import date
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from attendance.services.punch_service import PunchService
from attendance.services.attendance_service import AttendanceService

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


# 出勤ビュー呼び出し処理
@login_required
def punch_in_view(request):
    try:
        PunchService.punch_in(request.user)
        messages.success(request, "出勤しました")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("today")


# 退勤ビュー呼び出し処理
@login_required
def punch_out_view(request):
    try:
        PunchService.punch_out(request.user)
        messages.success(request, "退勤しました")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("today")

# # 出勤ボタン処理
# @login_required
# def punch_in(request):

#     if request.method != "POST":
#         return redirect("/")

#     today = timezone.now().date()

#     record, created = AttendanceRecord.objects.get_or_create(
#         user=request.user,
#         date=today
#     )

#     if record.clock_in:
#         messages.warning(request, "すでに出勤済です")
#         return redirect("attendance:today_attendance")

#     record.clock_in = timezone.now()
#     record.save()

#     messages.success(request, "出勤しました")

#     return redirect("attendance:today_attendance")

# # 退勤ボタン処理
# @login_required
# def punch_out(request):

#     if request.method != "POST":
#         return redirect("/")

#     today = timezone.now().date()

#     try:
#         record = AttendanceRecord.objects.get(
#             user=request.user,
#             date=today
#         )

#         if not record.clock_in:
#             messages.error(request, "出勤していません")
#             return redirect("attendance:today_attendance")

#         if record.clock_out:
#             messages.warning(request, "すでに退勤済です")
#             return redirect("attendance:today_attendance")

#         record.clock_out = timezone.now()
#         record.save()

#         messages.success(request, "退勤しました")

#     except AttendanceRecord.DoesNotExist:
#         messages.error(request, "出勤していません")

#     return redirect("attendance:today_attendance")

# 今日の勤怠表示ビュー処理
@login_required
def today_attendance(request):

    today = timezone.now().date()

    record = AttendanceRecord.objects.filter(
        user=request.user,
        date=today
    ).first()

    return render(
        request,
        "attendance/today_attendance.html",
        {"record": record}
    )

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


# 残業申請処理
@login_required
def overtime_request_create(request):

    if request.method == "POST":

        form = OvertimeRequestForm(request.POST)

        if form.is_valid():

            overtime = form.save(commit=False)
            overtime.user = request.user
            overtime.save()

            return redirect("attendance:overtime_request_list")

    else:
        form = OvertimeRequestForm()

    return render(
        request,
        "attendance/overtime_request.html",
        {"form": form}
    )

# 残業申請一覧ビュ
@login_required
def overtime_request_list(request):

    requests = OvertimeRequest.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(
        request,
        "attendance/overtime_request_list.html",
        {"requests": requests}
    )


# 上長承認リスト表示処理
@login_required
def leave_approval_list(request):

    if request.user.role != "manager":
        return redirect("/")

    requests = LeaveRequest.objects.filter(
        status="pending"
    ).order_by("date")

    return render(
        request,
        "attendance/leave_approval_list.html",
        {"requests": requests}
    )


# 承認ビュー
# @login_required
# def leave_approve(request, pk):

#     if request.method != "POST":
#         return redirect("/")

#     # leave = LeaveRequest.objects.get(
#     #     id=pk,
#     #     user__profile__manager=request.user
#     # )
#     leave = get_object_or_404(
#     LeaveRequest,
#     id=pk,
#     user__profile__manager=request.user
#     )

#     # leave.status = "approved"
#     # leave.save()
#     with transaction.atomic():

#         leave.status = "approved"
#         leave.save()

#     return redirect("attendance:leave_approval_list")

# # 却下ビュー
# @login_required
# def leave_reject(request, pk):

#     if request.method != "POST":
#         return redirect("/")

#     leave = LeaveRequest.objects.get(
#         id=pk,
#         user__profile__manager=request.user
#     )

#     leave.status = "rejected"
#     leave.save()

#     return redirect("attendance:leave_approval_list")

# 承認・却下ビュー
@login_required
def leave_update_status(request, pk, status):

    if request.method != "POST":
        return redirect("/")

    if status not in ["approved", "rejected"]:
        return redirect("/")

    leave = get_object_or_404(
        LeaveRequest,
        id=pk,
        user__profile__manager=request.user
    )

    with transaction.atomic():

        leave.status = status
        leave.save()

    return redirect("attendance:leave_approval_list")

@login_required
def monthly_attendance(request):

    data = AttendanceService.get_monthly_attendance(
        user=request.user,
        year=request.GET.get("year"),
        month=request.GET.get("month"),
    )

    return render(request, "attendance/monthly.html", data)

# # 勤怠一覧表示処理
# @login_required
# def monthly_attendance(request):

#     today = timezone.now().date()

#     year = int(request.GET.get("year", today.year))
#     month = int(request.GET.get("month", today.month))

#     # 月の日数取得
#     _, last_day = calendar.monthrange(year, month)

#     records = AttendanceRecord.objects.filter(
#         user=request.user,
#         date__year=year,
#         date__month=month
#     )

#     record_map = {r.date.day: r for r in records}

#     #休暇表示 
#     leaves = LeaveRequest.objects.filter(
#         user=request.user,
#         date__year=year,
#         date__month=month,
#         status="approved"
#     )

#     leave_map = {l.date.day: l for l in leaves}

#     days = []

#     for day in range(1, last_day + 1):

#         record = record_map.get(day)
#         leave = leave_map.get(day)

#         days.append({
#             "date": date(year, month, day),
#             "record": record,
#             "leave": leave
#         })

#     total_work = timedelta()

#     for d in days:

#         record = d["record"]

#         if record:
#             duration = record.work_duration()

#             if duration:
#                 total_work += duration




#     context = {
#         "days": days,
#         "year": year,
#         "month": month,
#         "total_work": total_work
#     }

#     return render(
#         request,
#         "attendance/monthly_attendance.html",
#         context
#     )