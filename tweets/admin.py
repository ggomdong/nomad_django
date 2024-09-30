from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "payload",
        "user",
        "total_likes",
        "created_at",
        "updated_at",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "tweet",
        "created_at",
        "updated_at",
    )