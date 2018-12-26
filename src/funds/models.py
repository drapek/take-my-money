from django.db import models
from djmoney.models.fields import MoneyField


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
    participants = models.ManyToManyField('users.User', through='Participation')

    @property
    def get_owner(self):
        return self.participants.filter(participation__is_owner=True).first()


class Participation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    is_enrolled = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    # user_payments = # TODO implement when Payment model will be done. There can be many payments made by one User.
