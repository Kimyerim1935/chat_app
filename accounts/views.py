from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib import messages
from .forms import RegisterForm
from .serializers import CreateUserSerializer
from .models import User, Profile
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .forms import CustomUserChangeForm, ProfileForm


# 회원가입
# class UserCreate(generics.CreateAPIView):
class UserCreateViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def SignUpView(request):
    if request.method == "POST":
        # 회원 가입 데이터 입력 완료
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        # 회원 가입 내용을 입력하는 상황
        user_form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form' : user_form})


def ProfileView(request, username): # urls.py에서 넘겨준 인자를 username으로 받는다.
    if not Profile.objects.filter(user=request.user):
        Profile.objects.create(user = request.user)
    user = get_object_or_404(get_user_model(), username=username)
    context = {'user':user}
    return render(request, 'accounts/profile.html', context)
# 프로필이 없으면 프로필 생성 페이지로 간다.
# 프로필이 있으면 프로필을 보여준다.

@login_required
def profile_update(request):
    user = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.profile_photo = request.POST.get('profile_photo')
            print(form.profile_photo)
            form.save()
            messages.success(request, '프로필을 수정/저장했습니다.')
            return redirect('accounts:profile', username=request.user)
    else:
        form = ProfileForm(instance=user)
    return render(request, 'accounts/profile_update.html', {
        'form': form
    })
