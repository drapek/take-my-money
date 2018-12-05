from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User as BaseUser, AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.models import IBANField
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('last_name', 'email')

    objects = UserManager()

    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# register signals
post_save.connect(create_auth_token, sender=User)
