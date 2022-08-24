from rest_framework import serializers
from interfaces.models import Interfaces


class InterfacesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    tester = serializers.CharField()
    projects = serializers.PrimaryKeyRelatedField()