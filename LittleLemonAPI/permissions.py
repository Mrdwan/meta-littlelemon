from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name="Manager").exists() or request.user.is_superuser
