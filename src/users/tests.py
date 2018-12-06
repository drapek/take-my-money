from django.test import TestCase

from rest_framework.test import APIClient

from core.tests import TestMixin
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


class UserDetailTestCase(TestCase, TestMixin):

    EXAMPLE_TEST_USER = {
            'username': 'test_user',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'test@test.test',
            'iban': 'DE89370400440532013000'
        }

    def setUp(self):
        self.api_client = APIClient()

    def test_successful_user_fetch(self):
        u = User.objects.create(**self.EXAMPLE_TEST_USER)
        self.api_client.force_authenticate(user=u)
        response = self.api_client.get(reverse('user-details', kwargs={'pk': u.pk}), format='json')
        self.assertDictKeys(response.data, ('username', 'email', 'first_name', 'last_name', 'iban'))
        u.delete()

    def test_successful_user_update(self):
        u = User.objects.create(**self.EXAMPLE_TEST_USER)
        data = self.EXAMPLE_TEST_USER
        data['first_name'] = "Zbyszek"
        self.api_client.force_authenticate(user=u)
        response = self.api_client.put(reverse('user-details', kwargs={'pk': u.pk}), data=data, format='json')
        self.assertEqual(response.data['first_name'], data["first_name"])
        self.assertEqual(User.objects.get(pk=u.pk).first_name, data['first_name'])
        u.delete()

    def test_successful_user_delete(self):
        pass

    def test_permissions_for_not_authenticated(self):
        pass

    def test_permissions_for_not_owner(self):
        pass

    def test_iban_update(self):
        pass