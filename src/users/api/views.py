from rest_framework import status, generics
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.permissions import IsHimself
from users.serializers import ChangePasswordSerializer, UserDetailsSerializer, UserInvitationSerializer, \
    UserRegistrationSerializer


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not instance.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            instance.set_password(serializer.data.get("new_password"))
            instance.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint for getting / updating / deleting User details. Permitted only to the owner.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated, IsHimself)

    def get_queryset(self):
        return User.objects.all()


class UserInvitation(generics.CreateAPIView):
    """
    Try to find user by username or email. If not exists it will send invitation via email.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = UserInvitationSerializer


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
