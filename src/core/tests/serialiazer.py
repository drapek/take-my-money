# This serialiazers are used only in testing.
from rest_framework import serializers

from core.tests.models import PermsTestOwnerField


class PermsTestOwnerFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermsTestOwnerField
        fields = '__all__'
