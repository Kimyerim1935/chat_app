from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from config import settings
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

app_name = 'accounts'
router = DefaultRouter()
router.register('accounts', UserCreateViewSet)

urlpatterns =[

    path('api-token-auth/', obtain_auth_token),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('allauth/', include('allauth.urls')),
    path('signup/', SignUpView, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('profile/<str:username>/', ProfileView, name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('', include(router.urls)),

 ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
