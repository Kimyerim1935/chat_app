from django.urls import path
from .views import *

urlpatterns = [
    path('<str:room_name>/', room, name='name'),
    path('', index, name='index'),
]