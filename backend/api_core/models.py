from django.db import models

class AuditoriaLogauditoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    accion = models.CharField(max_length=20)
    modulo = models.CharField(max_length=100)
    tabla_afectada = models.CharField(max_length=100)
    registro_id = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=39, blank=True, null=True)
    fecha = models.DateTimeField()
    usuario = models.ForeignKey('UsuarioUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auditoria_logauditoria'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class ClientesCliente(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo_persona = models.CharField(max_length=10)
    dni_cuit = models.CharField(unique=True, max_length=20)
    cuil = models.CharField(max_length=20, blank=True, null=True)
    condicion_iva = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    razon_social = models.CharField(max_length=200, blank=True, null=True)
    nombre_fantasia = models.CharField(max_length=200, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    domicilio_real = models.CharField(max_length=255)
    domicilio_fiscal = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField()
    estado = models.CharField(max_length=10)
    fecha_alta = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'clientes_cliente'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsuarioUsuario', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InventarioFotografiaVehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    archivo = models.CharField(max_length=100)
    nombre_original = models.CharField(max_length=255, blank=True, null=True)
    es_portada = models.IntegerField()
    tamano_bytes = models.IntegerField()
    mime_type = models.CharField(max_length=50)
    orden = models.PositiveIntegerField()
    fecha_alta = models.DateTimeField()
    vehiculo = models.ForeignKey('InventarioVehiculo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventario_fotografia_vehiculo'
        unique_together = (('vehiculo', 'orden'),)


class InventarioMarca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=100)
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'inventario_marca'


class InventarioModelo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=80)
    carroceria = models.CharField(max_length=20)
    updated_at = models.DateTimeField()
    marca = models.ForeignKey(InventarioMarca, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventario_modelo'


class InventarioTaller(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    estado = models.CharField(max_length=10)
    fecha_alta = models.DateField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'inventario_taller'


class InventarioTrasladovehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    costo_traslado = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    fecha_traslado = models.DateField()
    motivo = models.CharField(max_length=255)
    estado = models.CharField(max_length=15)
    fecha_alta = models.DateField()
    updated_at = models.DateTimeField()
    sucursal_destino = models.ForeignKey('SucursalSucursal', models.DO_NOTHING)
    sucursal_origen = models.ForeignKey('SucursalSucursal', models.DO_NOTHING, related_name='inventariotrasladovehiculo_sucursal_origen_set')
    usuario_autoriza = models.ForeignKey('UsuarioUsuario', models.DO_NOTHING)
    usuario_registro = models.ForeignKey('UsuarioUsuario', models.DO_NOTHING, related_name='inventariotrasladovehiculo_usuario_registro_set')
    vehiculo = models.ForeignKey('InventarioVehiculo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventario_trasladovehiculo'


class InventarioVehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    condicion_vehiculo = models.CharField(max_length=5)
    vin = models.CharField(unique=True, max_length=17, blank=True, null=True)
    patente = models.CharField(max_length=10, blank=True, null=True)
    anio = models.SmallIntegerField()
    color = models.CharField(max_length=50)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2)
    precio = models.DecimalField(max_digits=14, decimal_places=2)
    descripcion_tecnica = models.TextField()
    estado = models.CharField(max_length=20)
    kilometraje = models.IntegerField()
    activo = models.IntegerField()
    entregado = models.IntegerField()
    fecha_alta = models.DateTimeField()
    fecha_cambio_estado = models.DateTimeField(blank=True, null=True)
    combustible = models.CharField(max_length=15)
    transmision = models.CharField(max_length=15)
    puertas = models.SmallIntegerField()
    motor = models.CharField(max_length=50)
    traccion = models.CharField(max_length=15, blank=True, null=True)
    numero_serie_motor = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=20, blank=True, null=True)
    updated_at = models.DateTimeField()
    marca = models.ForeignKey(InventarioMarca, models.DO_NOTHING)
    modelo = models.ForeignKey(InventarioModelo, models.DO_NOTHING)
    sucursal = models.ForeignKey('SucursalSucursal', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventario_vehiculo'


class InventarioVehiculousado(models.Model):
    id = models.BigAutoField(primary_key=True)
    precio_info_auto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    porcentaje_deduccion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    precio_tasacion_final = models.DecimalField(max_digits=14, decimal_places=2)
    estado_cubierta = models.CharField(max_length=10, blank=True, null=True)
    estado_motor = models.CharField(max_length=10, blank=True, null=True)
    estado_chapa_pintura = models.CharField(max_length=10, blank=True, null=True)
    estado_interior = models.CharField(max_length=10, blank=True, null=True)
    fecha_evaluacion = models.DateField(blank=True, null=True)
    fecha_ingreso = models.DateField()
    observaciones = models.TextField()
    fecha_alta = models.DateField()
    updated_at = models.DateTimeField()
    taller = models.ForeignKey(InventarioTaller, models.DO_NOTHING, blank=True, null=True)
    usuario_autoriza = models.ForeignKey('UsuarioUsuario', models.DO_NOTHING)
    vehiculo = models.OneToOneField(InventarioVehiculo, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inventario_vehiculousado'


class ParametroSistema(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_parametro = models.CharField(unique=True, max_length=100)
    valor = models.CharField(max_length=255)
    tipo_dato = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True, null=True)
    fecha_alta = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'parametro_sistema'


class SucursalSucursal(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    estado = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'sucursal_sucursal'


class UsuarioRol(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'usuario_rol'


class UsuarioUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    estado = models.CharField(max_length=10)
    fecha_alta = models.DateField()
    updated_at = models.DateTimeField()
    sucursal = models.ForeignKey(SucursalSucursal, models.DO_NOTHING, blank=True, null=True)
    rol = models.ForeignKey(UsuarioRol, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_usuario'


class UsuarioUsuarioGroups(models.Model):
    usuario = models.ForeignKey(UsuarioUsuario, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usuario_usuario_groups'
        unique_together = (('usuario', 'group'),)


class UsuarioUsuarioUserPermissions(models.Model):
    usuario = models.ForeignKey(UsuarioUsuario, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'usuario_usuario_user_permissions'
        unique_together = (('usuario', 'permission'),)

