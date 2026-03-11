from django import forms
from .models import LeaveRequest

# 休暇申請フォーム
class LeaveRequestForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = LeaveRequest
        fields = ["date", "reason"]
    

    def clean(self):

        cleaned_data = super().clean()

        date = cleaned_data.get("date")

        if date and self.user:
            exists = LeaveRequest.objects.filter(
                user=self.user,
                date=date
            ).exists()

            if exists:
                raise forms.ValidationError(
                    "この日はすでに休暇申請しています"
                )
                
        return cleaned_data