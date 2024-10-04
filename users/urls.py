from django.urls import path
from . import views


urlpatterns = [
    path("<int:pk>/tweets/", views.Tweet.as_view()),
]
