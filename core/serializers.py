from rest_framework import serializers
from core.models import RequestCounter


class RequestCounterSerializer(serializers.Serializer):
    requests = serializers.IntegerField(source='count')

    class Meta:
        model = RequestCounter
        fields = ("requests",)
