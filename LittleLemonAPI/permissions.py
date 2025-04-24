from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name="Manager").exists() or request.user.is_superuser

class ReadOnlyOrIsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        # Reuse the IsManager logic
        manager_permission = IsManager()
        return manager_permission.has_permission(request, view)
