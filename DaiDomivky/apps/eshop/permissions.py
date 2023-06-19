from rest_framework import permissions

from .models import CANCELED


class IsOrderCanceled(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.order.status == CANCELED
