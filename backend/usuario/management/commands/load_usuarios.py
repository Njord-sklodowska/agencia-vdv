from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from usuario.models import Rol
from sucursal.models import Sucursal

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga roles y usuarios para pruebas del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("Iniciando carga de roles y usuarios..."))

        # 1. Definir y crear Roles
        roles_data = ['Administrador', 'Gerente', 'Vendedor']
        roles_objs = {}
        
        for r_nombre in roles_data:
            rol, created = Rol.objects.get_or_create(nombre=r_nombre)
            roles_objs[r_nombre] = rol
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {r_nombre}"))

        # 2. Obtener Sucursales
        sucursales = list(Sucursal.objects.all())
        if not sucursales:
            self.stderr.write(self.style.ERROR("No hay sucursales en la BD. Ejecuta primero la carga de sucursales."))
            return
        
        # 3. Definir Usuarios a crear
        # Formato: (username, password, rol_nombre, sucursal_obj)
        users_to_create = [
            # Admin Global
            ('admin_global', 'Pass123!', 'Administrador', None),
            
            # Gerentes por sucursal
            ('gerente_san_miguel', 'Pass123!', 'Gerente', sucursales[0]),
            ('gerente_concepcion', 'Pass123!', 'Gerente', sucursales[1]),
            ('gerente_banda', 'Pass123!', 'Gerente', sucursales[2]),
            
            # Vendedores San Miguel
            ('vendedor_sm1', 'Pass123!', 'Vendedor', sucursales[0]),
            ('vendedor_sm2', 'Pass123!', 'Vendedor', sucursales[0]),
            
            # Vendedores Concepción
            ('vendedor_con1', 'Pass123!', 'Vendedor', sucursales[1]),
            ('vendedor_con2', 'Pass123!', 'Vendedor', sucursales[1]),
            
            # Vendedores Banda
            ('vendedor_ban1', 'Pass123!', 'Vendedor', sucursales[2]),
            ('vendedor_ban2', 'Pass123!', 'Vendedor', sucursales[2]),
        ]

        success_count = 0
        
        for username, password, rol_name, sucursal in users_to_create:
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"Usuario {username} ya existe, saltando..."))
                continue
            
            try:
                # Creamos el usuario
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    rol=roles_objs[rol_name],
                    sucursal=sucursal,
                    is_staff=True if rol_name in ['Administrador', 'Gerente'] else False,
                    is_superuser=True if rol_name == 'Administrador' else False
                )
                
                self.stdout.write(self.style.SUCCESS(f"Usuario creado: {username} ({rol_name})"))
                success_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creando {username}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"\nCarga finalizada: {success_count} usuarios creados con éxito."))
        self.stdout.write(self.style.MIGRATE_LABEL("\nContraseña para todos los usuarios: Pass123!"))
