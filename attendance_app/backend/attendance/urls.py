from django.urls import path
from .views import (attendance_list, leave_request_create, leave_request_list, overtime_request_create, overtime_request_list, 
leave_approval_list, leave_update_status, monthly_attendance, today_attendance, punch_in_view, punch_out_view, approve_overtime, reject_overtime, overtime_by_department, monthly_report, export_monthly_csv)

app_name = "attendance"

urlpatterns = [
    path("list/", attendance_list, name="attendance_list"),
    path("leave/request/", leave_request_create, name="leave_request_create"),
    path("leave/list/", leave_request_list, name="leave_request_list"),
    path("overtime/request/", overtime_request_create, name="overtime_request_create"),
    path("overtime/", overtime_request_list, name="overtime_request_list"),
    path("leave/approval/", leave_approval_list, name="leave_approval_list"),
    path("leave/update/<int:pk>/<str:status>/", leave_update_status, name="leave_update_status"),
    path("monthly/", monthly_attendance, name="monthly_attendance"),
    path("today/", today_attendance, name="today"),
    path("punch/in/", punch_in_view, name="punch_in"),
    path("punch/out/", punch_out_view, name="punch_out"),
    path("overtime/<int:pk>/approve/", approve_overtime, name="approve_overtime"),
    path("overtime/<int:pk>/reject/", reject_overtime, name="reject_overtime"),
    path("overtime/department/", overtime_by_department, name="overtime_by_department"),
    path("report/monthly/", monthly_report, name="monthly_report"),
    path("report/monthly/csv/", export_monthly_csv, name="export_monthly_csv")
]