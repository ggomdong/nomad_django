from django.contrib import admin
from .models import Tweet, Like


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):

    class WordFilter(admin.SimpleListFilter):
        title = "Filter by words!"
        parameter_name = "word"

        def lookups(self, request, model_admin):
            # Custom Filter용 word 정의
            filter_word = "Elon Musk"

            return [
                (f"{filter_word}", f"contain {filter_word}"),
                (f"~{filter_word}", f"don't contain {filter_word}"),
            ]

        def queryset(self, request, tweets):
            word = self.value()

            # word가 존재하고, ~로 시작하지 않을 경우, word를 포함한 payload만 필터
            if word and not word.startswith("~"):
                return tweets.filter(payload__icontains=word)
            # word가 존재하고, ~로 시작할 경우, word를 포함한 payload를 제외
            elif word and word.startswith("~"):
                return tweets.exclude(payload__icontains=word[1:])
            else:
                tweets


    list_display = (
        "payload",
        "user",
        "user__username",
        "total_likes",
        "created_at",
        "updated_at",
    )

    list_filter = (
        WordFilter,
        "created_at",
    )

    search_fields = (
        "payload",
        "user__username",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user__username",
        "tweet",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
    )