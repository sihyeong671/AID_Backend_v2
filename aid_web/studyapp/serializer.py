from rest_framework import serializers

from .models import Study


class StudySerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(source="get_status_display", choices=Study.StatusType.choices, read_only=True)
    study_type = serializers.ChoiceField(
        source="get_study_type_display", choices=Study.StudyType.choices, read_only=True
    )

    class Meta:
        model = Study
        fields = "__all__"
