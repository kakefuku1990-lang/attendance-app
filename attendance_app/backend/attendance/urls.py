from django.urls import path
from .views import (punch_view, attendance_list, leave_request_create, leave_request_list, overtime_request_create, overtime_request_list, 
leave_approval_list, leave_update_status, monthly_attendance, today_attendance, punch_in_view, punch_out_view)

app_name = "attendance"

urlpatterns = [
    path("punch/", punch_view, name="punch"),
    path("list/", attendance_list, name="attendance_list"),
    path("leave/request/", leave_request_create, name="leave_request_create"),
    path("leave/list/", leave_request_list, name="leave_request_list"),
    path("overtime/request/", overtime_request_create, name="overtime_request_create"),
    path("overtime/", overtime_request_list, name="overtime_request_list"),
    path("leave/approval/", leave_approval_list, name="leave_approval_list"),
    # path("leave/approve/<int:pk>/", leave_approve, name="leave_approve"),
    # path("leave/reject/<int:pk>/", leave_reject, name="leave_reject"),
    path("leave/update/<int:pk>/<str:status>/", leave_update_status, name="leave_update_status"),
    path("monthly/", monthly_attendance, name="monthly_attendance"),
    path("today/", today_attendance, name="today_attendance"),
    # path("punch/in/", punch_in, name="punch_in"),
    # path("punch/out/", punch_out, name="punch_out"),
    path("punch/in/", punch_in_view, name="punch_in"),
    path("punch/out/", punch_out_view, name="punch_out"),
]