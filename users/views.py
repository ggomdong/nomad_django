from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer


@api_view()
def tweets(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise NotFound

    payload = user.tweets.all()
    serializer = UserSerializer(payload, many=True)
    return Response(serializer.data)
