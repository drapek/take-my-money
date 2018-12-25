from django.urls import reverse
from django.test import TestCase
from model_mommy import mommy
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from rest_framework.test import APIClient

from core.tests.models import PermsTestOwnerField
from users.models import User


class TestIsOwnerPermission(TestCase):
    """
    Tests IsOwner permission class used under REST framework.
    """
    def setUp(self):
        self.api_client = APIClient()
        self.permitted_user = mommy.make(User, iban="DE89370400440532013000")
        self.not_permitted_user = mommy.make(User, iban="PL61109010140000071219812874")
        self.api_client.force_authenticate(user=self.permitted_user)

    def test_no_perms_to_object(self):
        obj1 = PermsTestOwnerField.objects.create(owner=self.not_permitted_user)
        url = reverse("perms-owner-fields", kwargs={'pk': obj1.pk})
        response = self.api_client.get(url, format="json")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_perms_on_owner_field(self):
        obj1 = PermsTestOwnerField.objects.create(owner=self.permitted_user)
        url = reverse("perms-owner-fields", kwargs={'pk': obj1.pk})
        response = self.api_client.get(url, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
