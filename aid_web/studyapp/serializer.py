from rest_framework import serializers
from userapp.models import User

from .models import Study

# https://www.django-rest-framework.org/api-guide/relations/

# CRUD별로 다른 serializer를 써야할 때
# https://velog.io/@haremeat/Django-%ED%95%98%EB%82%98%EC%9D%98-APIView%EC%97%90%EC%84%9C-Serializerclass%EA%B0%80-%EB%8B%A4%EB%A5%BC-%EB%95%8C
# https://github.com/encode/django-rest-framework/issues/1563


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nick_name", "email")


class StudySerializer(serializers.ModelSerializer):
    leader = UserSerializer(many=False, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = "__all__"
