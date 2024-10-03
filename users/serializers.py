from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    payload = serializers.CharField()
    user = serializers.CharField()
