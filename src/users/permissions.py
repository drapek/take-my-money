from core.permissions import IsOwner


class IsHimself(IsOwner):
    fields_names_to_assert_with = []
