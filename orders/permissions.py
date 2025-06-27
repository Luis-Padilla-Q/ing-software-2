from rest_framework import permissions

class IsCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'perfil') and request.user.perfil.rol == 'cliente'

class IsRepartidor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'perfil') and request.user.perfil.rol == 'repartidor'

class IsEmpleado(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'perfil') and request.user.perfil.rol == 'empleado'

class IsAdminLocal(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'perfil') and request.user.perfil.rol == 'admin_local'
