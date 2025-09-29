from rest_framework import permissions


class IsOwnerOrAdminDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        if request.method in ["PUT", "PATCH"]:
            return obj == request.user

        if request.method == "DELETE":
            return request.user.is_staff or request.user.is_superuser

        return False