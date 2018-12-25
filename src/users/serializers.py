from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED

from users import models
from users.models import User, EmailInvitation


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    def update(self, instance, validated_data):
        pass

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer to get user details and update it. It can consist sensitive data.
    """

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'iban')


class UserInvitationSerializer(serializers.Serializer):
    """
    Serializer for creating user invitation.
    """
    email = serializers.EmailField(required=False)  # Email or username is required. See validate method.
    username = serializers.CharField(max_length=128, required=False)  # Email or username is required.
    # fund_id = serializers.IntegerField(required=True) # TODO implement it when Fund model will be done.

    def __init__(self, *args, **kwargs):
        super(UserInvitationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if hasattr(request, 'user'):
            self.request_user = request.user
        else:
            raise ValidationError("You are unauthorized.", code=HTTP_401_UNAUTHORIZED)

    # TODO implement when Fund will be done
    # def validate_fund_id(self, data):
    #     if Fund.objects.get(pk=data).owner != self.request_user:
    #         raise ValidationError("You don't have perms to add persons to this Fund")

    def validate(self, data):
        if "email" not in data and "username" not in data:
            raise ValidationError("Email or username property is needed.")
        return data

    def create(self, validated_data):
        invitation_receiver = User.objects.filter(Q(username=validated_data.get('username')) |
                                                  Q(email=validated_data.get('email'))).first()
        if invitation_receiver:
            pass  # TODO Assign invitation receiver to the Fund
            # return Fund
        else:
            recipient_email = validated_data.get('email')
            if not recipient_email:
                raise ValidationError("User with that data doesn't exists. And I can't send invitation because email "
                                      "property is empty.")
            # TODO assign Fund
            return EmailInvitation.objects.update_or_create(host=self.request_user, recipient_email=recipient_email)
