# This are urls used only in testing.

from django.urls import path

from core.tests.views import PermsTestOwnerFieldView

urlpatterns = [
    path("perms-owner-fields/<int:pk>/", PermsTestOwnerFieldView.as_view(), name='perms-owner-fields')
]

