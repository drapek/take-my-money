from django.test import TestCase

from rest_framework.test import APIClient

from users.models import User
from django.urls import reverse


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.test_user = User(username="tester1", last_name="Test")
        self.test_user.set_password("test1")
        self.test_user.save()

        self.api_client = APIClient()

    def test_token_generation_bad_password(self):
        data = {"username": "tester1", "password": "bad_one"}
        response = self.api_client.post(reverse('get-token'), data=data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_token_generation(self):
        data = {"username": "tester1", "password": "test1"}
        response = self.api_client.post(reverse('get-token'), data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_password_change_bad_password(self):
        data = {"old_password": "bad", "new_password": "asdasd123"}
        self.api_client.force_authenticate(user=self.test_user)
        response = self.api_client.put(reverse('reset-passwd'), data=data, format='json')
        self.api_client.force_authenticate(token=None)
        self.assertEqual(response.status_code, 400)

    def test_password_change_good(self):
        data = {"old_password": "test1", "new_password": "asdasd123"}
        self.api_client.force_authenticate(user=self.test_user)
        response = self.api_client.put(reverse('reset-passwd'), data=data, format='json')
        self.api_client.force_authenticate(token=None)
        self.assertEqual(response.status_code, 200)

    def test_password_not_authorized(self):
        data = {"old_password": "test1", "new_password": "asdasd123"}
        response = self.api_client.put(reverse('reset-passwd'), data=data, format='json')
        self.assertEqual(response.status_code, 401)
