from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    # https://ctrlzblog.com/user-registration-with-django-rest-framework/

    def has_permission(self, request, view):
        if view.action == "create":  # anyone can create user
            return True
        elif view.action == "list":
            return request.user.is_authenticated and request.user.is_staff
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            return True  # check in has_object_permission method
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif view.action in ["retrieve", "update", "partial_update", "destroy"]:
            return obj == request.user or request.user.is_staff
        else:
            return False
