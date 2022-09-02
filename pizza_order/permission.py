from rest_framework import permissions

from pizza_order.models import Shop


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Shop):
            return obj.owner == request.user
        else:
            return obj.user == request.user
