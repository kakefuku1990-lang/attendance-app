from django.urls import path
from .views import punch_view, attendance_list, leave_request_create, leave_request_list

app_name = "attendance"

urlpatterns = [
    path("punch/", punch_view, name="punch"),
    path("list/", attendance_list, name="attendance_list"),
    path("leave/request/", leave_request_create, name="leave_request_create"),
    path("leave/list/", leave_request_list, name="leave_request_list"),
]