from django.urls import path
from .views import punch_view, attendance_list

urlpatterns = [
    path("punch/", punch_view, name="punch"),
    path("list/", attendance_list, name="attendance_list"),
]