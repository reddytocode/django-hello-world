from django.test import TestCase
from rest_framework.test import APIClient


class CustomAPIClient():
    def __init__(self, test_case):
        self.app = APIClient()
        self.test_case = test_case

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


class BaseTest(TestCase):
    def setUp(self):
        self.app = CustomAPIClient(self)