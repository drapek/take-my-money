from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED

from funds.models import Fund
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


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new Users.
    """
    password = serializers.CharField(max_length=256, min_length=8)
    email = serializers.EmailField(required=False)  # If not given than default will be assigned. (form EmailInvitation)

    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'iban', 'password')

    def __init__(self, *args, **kwargs):
        super(UserRegistrationSerializer, self).__init__(*args, **kwargs)
        email_invitation_hash = kwargs.get('context').get('view').kwargs.get('hash')
        self.related_email_invitation = EmailInvitation.objects.get(id=email_invitation_hash)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return make_password(value)

    def validate_email(self, value):
        """
        If email is not given - assign the one from EmailInvitation
        """
        value = super(UserRegistrationSerializer, self).validate_email(self, value)
        if not value:
            return self.instance.receiver_email

    def validate(self, data):
        if self.related_email_invitation.is_used:
            raise ValidationError("This invitation has was already used.")
        return data

    def save(self, **kwargs):
        result = super(UserRegistrationSerializer, self).save(**kwargs)
        self.related_email_invitation.is_used = True  # Set EmailInvitation as used
        self.related_email_invitation.save()
        return result


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserInvitationSerializer(serializers.Serializer):
    """
    Serializer for creating user invitation.
    """
    email = serializers.EmailField(required=False)  # Email or username is required. See validate method.
    username = serializers.CharField(max_length=128, required=False)  # Email or username is required.
    # fund_id = serializers.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserInvitationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if hasattr(request, 'user'):
            self.request_user = request.user
        else:
            raise ValidationError("You are unauthorized.", code=HTTP_401_UNAUTHORIZED)

    def validate_fund_id(self, data):
        fund = Fund.objects.filter(pk=data).first()
        if not fund:
            raise ValidationError("fund_id invalid. Can't find Fund with this id.")

        if fund.get_owner != self.request_user:
            raise ValidationError("You don't have perms to add persons to this Fund")
        return data

    def validate(self, data):
        if "email" not in data and "username" not in data:
            raise ValidationError("Email or username property is needed.")
        return data

    def create(self, validated_data):
        invitation_receiver = User.objects.filter(Q(username=validated_data.get('username')) |
                                                  Q(email=validated_data.get('email'))).first()

        fund = Fund.objects.filter(pk=validated_data.get('fund_id')).first()
        if invitation_receiver:
            pass  # TODO Assign invitation receiver to the Fund. Make sure that this user is not already added.
            # return Fund
        else:
            recipient_email = validated_data.get('email')
            if not recipient_email:
                raise ValidationError("User with that data doesn't exists. And I can't send invitation because email "
                                      "property is empty.")
            return EmailInvitation.objects.create(host=self.request_user, recipient_email=recipient_email,
                                                  related_fund=fund)
