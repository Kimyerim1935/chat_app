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

