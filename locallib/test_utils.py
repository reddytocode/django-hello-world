from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class CustomAPIClient():
    def __init__(self, test_case):
        self.app = APIClient()
        self.test_case = test_case
        self.create_user()

    def get(self, url, data=None, status=None):
        response = self.app.get(url, data=data)
        if status:
            self.test_case.assertEqual(response.status_code, status)
        return response

    def post(self, url, data=None, status=None):
        response = self.app.post(url, data=data)
        if status:
            self.test_case.assertEqual(response.status_code, status)
        return response

    def delete(self, url, data=None, status=None):
        response = self.app.delete(url, data=data)
        if status:
            self.test_case.assertEqual(response.status_code, status)
        return response

    def patch(self, url, data=None, status=None):
        response = self.app.patch(url, data=data)
        if status:
            self.test_case.assertEqual(response.status_code, status)
        return response

    def login(self, user=None, password="1234"):
        url = reverse("users:token_obtain_pair")
        user = user if user else self.user
        response = self.app.post(url, data={"username": user.username, "password": password})
        access_token = response.data["access"]
        self.app.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def logout(self):
        self.app.credentials(HTTP_AUTHORIZATION="")

    def create_user(self):
        self.user = User.objects.create_user("user-1", password="1234")


class BaseTest(TestCase):
    def setUp(self):
        self.app = CustomAPIClient(self)

