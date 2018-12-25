from django.db import models
from django.db.models import SET_NULL
from djmoney.models.fields import MoneyField

from users.models import User


class Fund(models.Model):

    FUND_STATE = (
        (0, "Participants collecting"),
        (1, "Money collecting"),
        (-1, "Inactive"),
    )

    image_cover = models.ImageField(upload_to='funds_cover_photos/', null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=8192)
    due_date = models.DateTimeField()
    amount_to_collect = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='PLN',
        max_digits=10
    )
    state = models.IntegerField(choices=FUND_STATE, default=0)
    participants = models.ManyToManyField(User, through='Participation')


class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    is_enrolled = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    # user_payments = # TODO implement when Payment model will be done. There can be many payments made by one User.
