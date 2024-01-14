from typing import Any

from rest_framework import serializers
from userapp.models import User

from .models import Study, StudyUserRelation

# https://www.django-rest-framework.org/api-guide/relations/

# CRUD별로 다른 serializer를 써야할 때
# https://velog.io/@haremeat/Django-%ED%95%98%EB%82%98%EC%9D%98-APIView%EC%97%90%EC%84%9C-Serializerclass%EA%B0%80-%EB%8B%A4%EB%A5%BC-%EB%95%8C
# https://github.com/encode/django-rest-framework/issues/1563


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "nick_name", "email")


class StudyUserSerializer(serializers.Serializer):
    study_name = serializers.CharField(source="study.study_name")
    user_email = serializers.CharField(source="user.email")
    is_approve = serializers.BooleanField()

    class Meta:
        model = StudyUserRelation
        fields = ("study_name", "user_email", "is_approve")


class StudySerializer(serializers.ModelSerializer):
    status_readable = serializers.ChoiceField(
        source="get_status_display", choices=Study.StatusType.choices, read_only=True
    )
    leader = UserSerializer(many=False, read_only=True)
    users = StudyUserSerializer(many=True, read_only=True, source="studyuserrelation_set")
    # users_waiting = UserSerializer(many=True, read_only=True)

    def create(self, validated_data: dict[str, Any]) -> Study:
        leader = validated_data["leader"]
        instance = Study.objects.create(**validated_data)

        studyuserrelation_set = [StudyUserRelation(user_id=leader.id, study_id=instance.id, is_approve=True)]
        instance.studyuserrelation_set.add(*studyuserrelation_set, bulk=False)

        return instance

    class Meta:
        model = Study
        fields = "__all__"
