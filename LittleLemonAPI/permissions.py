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

class CanAccessOrderDetails(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        is_manager = request.user.groups.filter(name="Manager").exists() or request.user.is_superuser
        is_delivery_crew = request.user.groups.filter(name="Delivery crew").exists()

        if request.method in permissions.SAFE_METHODS:
            if is_manager:
                return True
            if is_delivery_crew:
                return obj.delivery_crew == request.user
            return obj.user == request.user

        if request.method in ['PUT', 'PATCH']:
            if is_manager:
                return True
            if is_delivery_crew:
                allowed_keys = {'status'}
                update_keys = set(request.data.keys())
                return update_keys.issubset(allowed_keys) and obj.delivery_crew == request.user

            return False

        if request.method == 'DELETE':
            return is_manager

        return False
