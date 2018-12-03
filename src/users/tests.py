from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient

from users.models import User
from django.urls import reverse


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        test_user = User(username="tester1", last_name="Test")
        test_user.set_password("test1")

        self.api_client = APIClient()

    def test_token_generation_bad_passwd(self):
        data = {"username": "tester1", "password": "bad_one"}
        response = self.api_client.post(reverse('get_token'), data=data)
        assert response.status_code == 404

    def test_token_generation(self):
        data = {"username": "tester1", "password": "test1"}
        response = self.api_client.post('get_token', data=data)
        assert response.status_code == 200
        print(response.data)
