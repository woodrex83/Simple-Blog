from django import forms
from .models import User

class ProfileForm(forms.Form):
    class Meta:
        model = User
        # 前端顯示可修改的字段
        fields = ['nickname', 'avatar']