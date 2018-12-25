# This views are used only in testing.

from rest_framework import generics

from core.permissions import IsOwner
from core.tests.models import PermsTestOwnerField
from core.tests.serialiazer import PermsTestOwnerFieldSerializer


class PermsTestOwnerFieldView(generics.RetrieveAPIView):
    permission_classes = (IsOwner,)
    serializer_class = PermsTestOwnerFieldSerializer
    queryset = PermsTestOwnerField.objects.all()
