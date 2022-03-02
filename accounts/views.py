from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView

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
    profile = get_object_or_404(User, username=username)
    return render(request, 'accounts/profile.html', {'profile':profile})


class ProfileUpdateView(View): # 간단한 View클래스를 상속 받았으므로 get함수와 post함수를 각각 만들어줘야한다.
    # 프로필 편집에서 보여주기위한 get 메소드
    def get(self, request):
        user = get_object_or_404(get_user_model(), pk=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = CustomUserChangeForm(initial={
            'email': user.email,
            'username': user.username,
            'name': user.name
        })

        if hasattr(user, 'profile'):  # user가 profile을 가지고 있으면 True, 없으면 False (회원가입을 한다고 profile을 가지고 있진 않으므로)
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': profile.nickname,
                'description': profile.description,
                'profile_photo': profile.profile_photo,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'accounts/profile_update.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = CustomUserChangeForm(request.POST, instance=u)  # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        # User 폼
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)  # 기존의 것 가져와 수정하는 것
        else:
            profile_form = ProfileForm(request.POST, request.FILES)  # 새로 만드는 것

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)  # 기존의 것을 가져와 수정하는 경우가 아닌 새로 만든 경우 user를 지정해줘야 하므로
            profile.user = u
            profile.save()

        return redirect('accounts:profile', pk=request.user.username)  # 수정된 화면 보여주기