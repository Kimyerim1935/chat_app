from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label="이메일")
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']
        labels = {
            'username': '아이디',
            'password': '비밀번호',
            'password2': '비밀번호 확인',
            'email': '이메일',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('비밀번호 확인이 일치하지 않습니다.')
        return cd['password2']