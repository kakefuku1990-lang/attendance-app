from django.shortcuts import get_object_or_404
from attendance.models import OvertimeRequest


class OvertimeService:

    @staticmethod
    def approve(user, pk):

        overtime = get_object_or_404(OvertimeRequest, pk=pk)

        if user.role not in ["manager", "admin"]:
            raise ValueError("権限がありません")

        overtime.status = "approved"
        overtime.save()

        return overtime

    @staticmethod
    def reject(user, pk):

        overtime = get_object_or_404(OvertimeRequest, pk=pk)

        if user.role not in ["manager", "admin"]:
            raise ValueError("権限がありません")

        overtime.status = "rejected"
        overtime.save()

        return overtime