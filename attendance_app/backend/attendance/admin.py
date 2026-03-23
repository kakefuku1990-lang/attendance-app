# Register your models here.
from django.contrib import admin
from .models import AttendanceRecord
from .models import Profile, Department
from .models import AttendanceCorrectionRequest
from .models import LeaveRequest
from .models import OvertimeRequest

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


# 申請機能設定
@admin.register(AttendanceCorrectionRequest)
class AttendanceCorrectionRequestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "date",
        "status",
        "created_at",
    )

    list_filter = ("status", "date")

# 休暇申請設定
@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "date",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

# 残業申請設定
@admin.register(OvertimeRequest)
class OvertimeRequestAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "date",
        "hours",
        "status",
    )

    list_filter = ("status",)