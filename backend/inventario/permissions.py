from rest_framework.permissions import BasePermission

JERARQUIA_ROLES = {
    'superadministrador': 4,
    'gerente': 3,
    'administrativo': 2,
    'vendedor': 1,
}


def nivel_rol(usuario):
    if usuario.is_superuser:
        return 99
    if not usuario.rol:
        return 0
    return JERARQUIA_ROLES.get(usuario.rol.nombre, 0)


class EsAdministrativoOSuperior(BasePermission):
    """Permite acciones solo a Administrativo, Gerente o Superadministrador."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return nivel_rol(request.user) >= JERARQUIA_ROLES['administrativo']


class EsGerenteOSuperior(BasePermission):
    """Permite acciones solo a Gerente o Superadministrador."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return nivel_rol(request.user) >= JERARQUIA_ROLES['gerente']


class EsSuperadministrador(BasePermission):
    """Permite acciones solo al Superadministrador."""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return nivel_rol(request.user) >= JERARQUIA_ROLES['superadministrador']