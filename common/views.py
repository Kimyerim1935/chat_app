from django.shortcuts import render
from .forms import RegisterForm

# CRUD Create, Update

def signup(request):
    if request.method == "POST":
        # 회원 가입 데이터 입력 완료
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'common/register_done.html', {'new_user': new_user})
    else:
        # 회원 가입 내용을 입력하는 상황
        user_form = RegisterForm()
    return render(request, 'common/signup.html', {'form' : user_form})