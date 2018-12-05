from rest_framework import serializers

from users import models


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    def update(self, instance, validated_data):
        pass

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserDetailsSerializer(serializers.Serializer):
    """
    Serializer to get user details and update it. It can consist sensitive data.
    """

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'iban')

    def update(self, instance, validated_data):
        pass
