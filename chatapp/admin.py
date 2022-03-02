from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):

    list_display = ['id', 'room_name']
    list_display_links = ['room_name']

class MessageAdmin(admin.ModelAdmin):

    list_display = ['user', 'room', 'content', 'created']
    list_display_links = ['user', 'room', 'content', 'created']


