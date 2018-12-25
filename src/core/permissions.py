from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    This permission will check if given model has proper user field (defined in @fields_names_to_assert_with list)
    And if id of this user field is equal with id of user that is making the request.
    """
    fields_names_to_assert_with = ['user', 'owner']

    def has_object_permission(self, request, view, obj):
        for field_to_check in self.fields_names_to_assert_with:
            if hasattr(obj, field_to_check):
                if getattr(obj, field_to_check) == request.user:
                    return True
                else:
                    return False
        else:
            # If fields_names_to_assert_with is empty, it means to treat object as user, to its field.
            return obj == request.user

