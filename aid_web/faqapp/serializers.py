from rest_framework import serializers

from .models import FAQ


class FQASerializers(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
