from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField(
        User, # 유저 모델과 연결
        related_name='rooms' # 룸 인덱스명 지정
    )

    def __str__(self):
        return self.room_name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_message')
    room = models.ForeignKey(Room, related_name='messages', default=1, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Chat_Connection(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_target') # 상대방
    room = models.ForeignKey(Room, blank=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user') # 나
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "채팅" # 사용자명 반환

