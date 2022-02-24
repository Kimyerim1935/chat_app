from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('accounts', UserCreateViewSet)

urlpatterns =[

    path('api-token-auth/', obtain_auth_token),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', include(router.urls)),
    # path('signup/', UserCreate.as_view()),


 ]


