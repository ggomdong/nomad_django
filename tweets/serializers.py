from rest_framework import serializers


class TweetSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    payload = serializers.CharField(
        max_length=180,
    )
    user = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
