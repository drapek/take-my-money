# This models are used only in testing.
from django.db import models
from django.db.models import CASCADE

from users.models import User


class PermsTestOwnerField(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    field1 = models.TextField(default="abcdefg", max_length=32)
