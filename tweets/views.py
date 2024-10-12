from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Tweet
from . import serializers


class Tweets(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    # See all tweets
    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = serializers.TweetSerializer(all_tweets, many=True)
        return Response(serializer.data)

    # Create a tweet
    def post(self, request):
        serializer = serializers.TweetSerializer(data=request.data)
        if serializer.is_valid():
            tweet = serializer.save(user=request.user)
            return Response(serializers.TweetSerializer(tweet).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class TweetDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound

    # See a tweet
    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = serializers.TweetSerializer(tweet)
        return Response(serializer.data)

    # Edit a tweet
    def put(self, request, pk):
        tweet = self.get_object(pk)
        serializer = serializers.TweetSerializer(
            tweet,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            tweet = serializer.save()
            return Response(serializers.TweetSerializer(tweet).data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    # Delete a tweet
    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=HTTP_200_OK)
