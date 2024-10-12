from rest_framework.test import APITestCase
from .models import Tweet
from users.models import User


# Test GET and POST methods
class TestTweets(APITestCase):
    # tweet 생성을 위해서는 user가 필수이므로, user 정보를 세팅
    USER_DICT = {
        "username": "test",
        "email": "test@test.com",
        "name": "testname",
        "is_host": False,
        "gender": "male",
        "language": "kr",
        "currency": "won",
        "password": "123",
    }
    PAYLOAD = "Test Tweet"
    URL = "/api/v1/tweets/"

    user = User(**USER_DICT)

    def setUp(self):
        self.user.save()

        Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    def test_all_tweets(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["payload"],
            self.PAYLOAD,
        )
        self.assertEqual(
            data[0]["user"]["username"],
            self.USER_DICT["username"],
        )

    def test_create_tweet(self):
        # tweet 생성 시 인증이 필요하므로, 강제로 로그인 처리
        self.client.force_login(
            self.user,
        )
        response = self.client.post(
            self.URL,
            data={
                "user": self.user,
                "payload": self.PAYLOAD,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )

        # post 시 data를 부여하지 않고, 강제로 오류를 발생시킴
        # views.py 에서 validation 실패 시 HTTP_400_BAD_REQUEST를 발생하도록 수정하였고, tests.py에서 확인
        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            400,
        )
        self.assertIn(
            "payload",
            data,
        )


# Test GET, PUT and DELETE methods
class TestTweet(APITestCase):
    # tweet 생성을 위해서는 user가 필수이므로, user 정보를 세팅
    USER_DICT = {
        "username": "test",
        "email": "test@test.com",
        "name": "testname",
        "is_host": False,
        "gender": "male",
        "language": "kr",
        "currency": "won",
        "password": "123",
    }
    PAYLOAD = "Test Tweet"
    NEW_PAYLOAD = "New Tweet"
    URL = "/api/v1/tweets/1"

    user = User(**USER_DICT)

    def setUp(self):
        self.user.save()

        Tweet.objects.create(
            user=self.user,
            payload=self.PAYLOAD,
        )

    # 존재하지 않는 경로 테스트
    def test_tweet_not_found(self):
        response = self.client.get(self.URL + "2")

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_get_tweet(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertIsInstance(
            data,
            dict,
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
        )
        self.assertEqual(
            data["user"]["username"],
            self.USER_DICT["username"],
        )

    def test_put_tweet(self):
        # tweet 수정 시 인증이 필요하므로, 강제로 로그인 처리
        self.client.force_login(
            self.user,
        )
        response = self.client.put(
            self.URL,
            data={
                "user": self.user,
                "payload": self.NEW_PAYLOAD,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
        self.assertEqual(
            data["payload"],
            self.NEW_PAYLOAD,
        )

    def test_delete_tweet(self):
        # tweet 삭제 시 인증이 필요하므로, 강제로 로그인 처리
        self.client.force_login(
            self.user,
        )

        response = self.client.delete(self.URL)

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200.",
        )
