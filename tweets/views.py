from django.shortcuts import render
from .models import Tweet


def see_all_tweets(request):
    tweets = Tweet.objects.all()

    context = {'title': 'All Tweets', 'tweets': tweets,}

    return render(request, "all_tweets.html", context)