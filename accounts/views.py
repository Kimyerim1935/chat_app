from django.shortcuts import render

from .forms import RegisterForm
from .serializers import CreateUserSerializer
from .models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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
