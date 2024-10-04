from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from tweets.serializers import TweetSerializer


class Tweet(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)

        payload = user.tweets.all()
        serializer = TweetSerializer(payload, many=True)
        return Response(serializer.data)
