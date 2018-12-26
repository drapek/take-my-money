import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User as BaseUser, AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models import SET_NULL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.models import IBANField
from rest_framework.authtoken.models import Token

from funds.models import Fund
from settings.base import DEFAULT_FROM_EMAIL
from settings.base import FRONTEND_DOMAIN
from settings.base import PORTAL_NAME


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
    iban = IBANField(include_countries=IBAN_SEPA_COUNTRIES, null=True, default=None)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class EmailInvitation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    host = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    date = models.DateTimeField(auto_now=True, null=False)
    recipient_email = models.EmailField()
    is_used = models.BooleanField(default=False)
    related_fund = models.ForeignKey(Fund, on_delete=SET_NULL, null=True)

    @property
    def get_fund_name(self):
        if self.related_fund:
            return self.related_fund.name
        else:
            "-"

    def send_email_invitation(self):
        send_mail(
            subject=f'{PORTAL_NAME} - Invitation to participate in {self.get_fund_name}.',
            message=render_to_string('users/email_invitation.html', {'event_name': f"{self.get_fund_name}",
                                                                     'portal_name': PORTAL_NAME,
                                                                     'host': self.host.username,
                                                                     'fund': self.related_fund,
                                                                     'url': f'{FRONTEND_DOMAIN}/register/{self.id}'
                                                                     }),
            from_email=f'{DEFAULT_FROM_EMAIL}',
            recipient_list=(self.recipient_email, )
        )


@receiver(post_save, sender=EmailInvitation)
def trigger_send_email_invitation(sender, instance=None, created=False, **kwargs):
    instance.send_email_invitation()
