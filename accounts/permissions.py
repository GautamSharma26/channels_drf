from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Using IsOwner class to implement in our class to access only by such user who is authorized
     for that specific functionality  .
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
