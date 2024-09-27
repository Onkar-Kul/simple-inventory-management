from rest_framework.permissions import BasePermission


class IsItemAdder(BasePermission):
    """
    Custom permission to only allow users who can add items.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_item_adder)
