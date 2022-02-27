from django.urls import path
from .views import *

app_name = 'chatapp'

urlpatterns = [
    path('<str:room_name>/', room, name='name'),
    path('', index, name='index'),
]