from .models import User
from rest_framework.serializers import ModelSerializer



class CreateUserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password']


"""
UserSerializer에서는 한 가지 주의해야 할 점이 있는데,

바로 create 시 (회원가입 시) 입력받은 데이터를 검증해주어야 한다는 것입니다.

(유효하지 않은 값의 입력을 방지하기 위해)
"""