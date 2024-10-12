from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status
from .models import User
from . import serializers
from tweets.serializers import TweetSerializer


class Users(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    # See all users
    def get(self, request):
        all_users = User.objects.all()
        serializer = serializers.PrivateUserSerializer(all_users, many=True)
        return Response(serializer.data)

    # Create a user account with password
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("Password is needed.")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response(serializers.PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)


class Me(APIView):

    permission_classes = [IsAuthenticated]

    # 본인의 프로필을 확인하는 기능
    # 인증만 되면 추가 변수없이도 GET을 테스트할 수 있으므로, Authentication Test를 위해 생성
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializers.PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    # See user profile
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class Tweet(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    # See tweets by a user
    def get(self, request, pk):
        user = self.get_object(pk)

        payload = user.tweets.all()
        serializer = TweetSerializer(payload, many=True)
        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    # Change password of logged in user
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Old or New Password is missing.")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError("There is no user or entered password is wrong.")


class LogIn(APIView):
    # Log user in
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username and password are needed.")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Wrong password"})


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    # Log user out
    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
