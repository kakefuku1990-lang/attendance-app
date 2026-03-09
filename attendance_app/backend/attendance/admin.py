from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AttendanceRecord

from .models import Profile, Department

# 打刻履歴モデルの管理画面
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "date",
        "clock_in",
        "clock_out"
    )

    list_filter = ("date", "user")

    search_fields = ("user__username",)

# 社員情報モデルの管理画面
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "employee_id", "department")


admin.site.register(Profile, ProfileAdmin)

# 部署情報モデルの管理画面
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(Department, DepartmentAdmin)