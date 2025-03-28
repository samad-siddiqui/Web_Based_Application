from django.test import TestCase
from django.test.client import Client
from http import HTTPStatus
from users.models import UserRole, CustomUser, Profile
from django.utils.timezone import now
import time


class TestLoggingMiddleware(TestCase):

    def setUp(self):
        self.client = Client()
        self.gold_user = CustomUser.objects.create_user(
            email="gold@example.com", password="test123"
            )
        self.bronze_user = CustomUser.objects.create_user(
            email="bronze@example.com", password="test123"
            )
        self.silver_user = CustomUser.objects.create_user(
            email="silver@example.com", password="test123"
        )

        self.gold_user.profile.status = UserRole.GOLD
        self.gold_user.profile.save()
        self.silver_user.profile.status = UserRole.SILVER
        self.silver_user.profile.save()
        self.bronze_user.profile.status = UserRole.BRONZE
        self.bronze_user.profile.save()

    def test_logging_middleware(self):
        print("test_logging_middleware")
        self.client.login(email="bronze@example.com", password="test123")
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_ip_extraction(self):
        print("test_ip_extraction")
        self.client.login(email="gold@example.com", password="test123")
        response = self.client.get('/', HTTP_X_FORWARDED_FOR='123.45.67.89')
        print(response)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_rate_limiting(self):
        print("test_rate_limiting")
        self.client.login(email="silver@example.com", password="test123")
        for i in range(5):
            response = self.client.get("/profile/")
            self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, HTTPStatus.TOO_MANY_REQUESTS)

    def test_rate_limit_reset(self):
        print("test_rate_limit_reset")
        self.client.login(email="silver@example.com", password="test123")
        profile = Profile.objects.get(user=self.silver_user)
        profile.last_hit = now()
        profile.count = 0
        profile.save()
        for i in range(5):
            response = self.client.get("/profile/")
            self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, HTTPStatus.TOO_MANY_REQUESTS)
        time.sleep(61)
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
