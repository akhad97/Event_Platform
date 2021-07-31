from rest_framework import permissions
from .models import *

class IsOrganizer(permissions.BasePermission):
   def has_permission(self, request, view):
       if request.user.is_authenticated and request.user.is_organizer:
           return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

