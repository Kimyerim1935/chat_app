from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from config import settings
from django.contrib.auth import get_user_model

class UserManager(BaseUserManager): # 유저 생성하는 헬퍼 클래스
    # 일반 user 생성
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not username:
            raise ValueError('must have user username')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, username, name, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin): # 실제 모델을 상속받아 생성하는 클래스
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    username = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 username으로 설정
    USERNAME_FIELD = 'username'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 현 계정의 사용자를 가져올 수 있음.
    nickname = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True) # 값을 채워넣지 않아도 되는 속성.
