from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from model_mommy import mommy
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, \
    HTTP_401_UNAUTHORIZED, HTTP_201_CREATED

from rest_framework.test import APIClient

from core.mixins import TestMixin
from users.models import User, EmailInvitation
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

    EXAMPLE_TEST_USER_2 = {
        'username': 'test_user2',
        'first_name': 'first_name2',
        'last_name': 'last_name2',
        'email': 'test2@test.test',
        'iban': 'PL61 1090 1014 0000 0712 1981 2874'
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
        u = User.objects.create(**self.EXAMPLE_TEST_USER)
        self.assertTrue(User.objects.get(pk=u.pk))
        self.api_client.force_authenticate(user=u)
        response = self.api_client.delete(reverse('user-details', kwargs={'pk': u.pk}))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=u.pk)

    def test_permissions_for_not_authenticated(self):
        # Try to make action on user data as unauthenticated User
        u1 = User.objects.create(**self.EXAMPLE_TEST_USER)
        response = self.api_client.get(reverse('user-details', kwargs={'pk': u1.pk}))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

        # Try to make action on user data of another User
        u2 = User.objects.create(**self.EXAMPLE_TEST_USER_2)
        self.api_client.force_authenticate(user=u1)
        response = self.api_client.get(reverse('user-details', kwargs={'pk': u2.pk}))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_successful_iban_update(self):
        u = User.objects.create(**self.EXAMPLE_TEST_USER)
        self.api_client.force_authenticate(user=u)

        user_new_iban = self.EXAMPLE_TEST_USER
        user_new_iban.update({
            'iban': 'PL61109010140000071219812874'
        })

        response = self.api_client.put(reverse('user-details', kwargs={'pk': u.pk}), data=user_new_iban, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=u.pk).iban, user_new_iban['iban'])

    def test_invalid_iban_update(self):
        u = User.objects.create(**self.EXAMPLE_TEST_USER)
        self.api_client.force_authenticate(user=u)

        user_new_iban = self.EXAMPLE_TEST_USER
        user_new_iban.update({
            'iban': 'PL88888888888888888888888888'
        })

        response = self.api_client.put(reverse('user-details', kwargs={'pk': u.pk}), data=user_new_iban, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotEqual(User.objects.get(pk=u.pk).iban, user_new_iban['iban'])


class UserInvitationTestCase(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user_1 = mommy.make(User)
        self.user_2 = mommy.make(User)
        self.api_client.force_authenticate(user=self.user_1)

    def test_creation_invitation_email(self):
        """
        Test if invitation email is send when we get email at the endpoint that doesn't exists.
        """
        data = {
            'email': "notexistingemail@test.test",
            # 'fund_id': fund.id   # TODO implement it when Fund model will be done.
        }
        response = self.api_client.post(reverse('user-invitation'), data=data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(EmailInvitation.objects.count(), 1)

    def test_assigning_existing_user(self):
        """
        Check if for existing user (email or username exists in DB) we assigned it to proper Fund
        """
        pass  # TODO impelment when Fund model will be done

    def test_successful_user_registration_via_url(self):
        pass
