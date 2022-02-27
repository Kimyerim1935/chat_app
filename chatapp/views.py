from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='accounts:login')
def index(request):
    return render(request, 'chatapp/index.html')

@login_required(login_url='accounts:login')
def room(request, room_name):
    return render(request, 'chatapp/room.html', {'room_name': room_name})
