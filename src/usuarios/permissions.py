
#IMPORTANTE EN LA DB TENER TRES GROUPS CARGADOS PARA QUE FUNCIONEN LOS PERMISOS.
#SE DEBE CARGAR MANUALMENTE ROL DE Usuario Y Vendedor


from rest_framework import permissions

class PermissionVendedor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.groups.filter(name__in=['Vendedor']).exists() or request.user.is_superuser)

class PermissionUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.groups.filter(name__in=['Usuario']).exists() or request.user.is_superuser)