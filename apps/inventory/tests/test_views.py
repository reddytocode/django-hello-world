from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class ProductListTests(TestCase):
    def setUp(self):
        self.app = APIClient()
        self.url = reverse("inventory:product-list")

    def test_list(self):
        response = self.app.get(self.url)
        self.assertEqual(response.status_code, 200)
