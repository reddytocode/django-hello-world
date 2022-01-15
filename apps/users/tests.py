from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from locallib.test_utils import BaseTest


class UserTests(BaseTest):
    def setUp(self):
        super().setUp()
        self.data = {
            "username": "Asdf",
            "password": "1234dff"
        }
        self.url = reverse("users:token_obtain_pair")

    def test_get_token(self):
        User.objects.create_user("Asdf", password="1234dff")
        response = self.app.post(self.url, data=self.data)
        access_token = response.data["access"]
        self.assertTrue(len(access_token) > 1)
