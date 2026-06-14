
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
import datetime
import mimetypes

from django.core.exceptions import ValidationError, PermissionDenied
from django.conf import settings

# Marca =============================================================================
class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
# Modelo ==============================================================================

class Modelo(models.Model):
    CARROCERIA_CHOICES = [
        ('sedan', 'Sedán'), ('hatchback', 'Hatchback'), ('suv', 'SUV'),
        ('pickup', 'Pickup'), ('camioneta', 'Camioneta'), ('furgon', 'Furgón'),
        ('coupe', 'Coupé'), ('familiar', 'Familiar'), ('crossover', 'Crossover'),
        ('minivan', 'Minivan'), ('otro', 'Otro')
    ]
    
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='modelos')
    nombre = models.CharField(max_length=80)
    carroceria = models.CharField(max_length=20, choices=CARROCERIA_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['marca', 'nombre'], name='unique_modelo_por_marca')
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"
    
# Vehiculo =====================================================================================
    
vin_validator = RegexValidator(
    regex=r'^[A-HJ-NPR-Z0-9]{17}$',
    message="El VIN debe tener 17 caracteres alfanuméricos y no puede incluir las letras I, O ni Q.",
    code='invalid_vin'
)

class Vehiculo(models.Model):
    # Enums
    CONDICION_CHOICES = [('0km', '0km'), ('usado', 'Usado')]
    ESTADO_CHOICES = [('en_stock', 'En Stock'), ('reservado', 'Reservado'), ('vendido', 'Vendido')]
    COMBUSTIBLE_CHOICES = [('nafta', 'Nafta'), ('diesel', 'Diesel'), ('gnc', 'GNC'), ('hibrido', 'Híbrido'), ('electrico', 'Eléctrico')]
    TRANSMISION_CHOICES = [('manual', 'Manual'), ('automatica', 'Automática')]
    TRACCION_CHOICES = [('delantera', 'Delantera'), ('trasera', 'Trasera'), ('4x4', '4x4')]
    PROCEDENCIA_CHOICES = [('compra_directa', 'Compra Directa'), ('parte_de_pago', 'Parte de Pago')]
    
    # Relaciones
    sucursal = models.ForeignKey('sucursal.Sucursal', on_delete=models.PROTECT, related_name='vehiculos')
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, on_delete=models.PROTECT)

    # caracteristicas del vehiculo
    condicion_vehiculo = models.CharField(max_length=5, choices=CONDICION_CHOICES)
    
    vin = models.CharField(max_length=17,unique=True,null=True, blank=False, validators=[vin_validator],help_text="Ingrese el número de chasis (VIN) de 17 caracteres."
    )

    patente = models.CharField(max_length=10, null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patente'], 
                name='unique_patente_no_nula', 
                condition=models.Q(patente__isnull=False)
            )
        ]
    anio = models.SmallIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(datetime.date.today().year + 1)])
    color = models.CharField(max_length=50)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2) # Lógica de visibilidad en Serializer
    precio = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.01)])
    descripcion_tecnica = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_stock')
    kilometraje = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    entregado = models.BooleanField(default=False)

    # Fechas
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_cambio_estado = models.DateTimeField(null=True, blank=True)
    
    # Especificaciones técnicas de vehiculo
    combustible = models.CharField(max_length=15, choices=COMBUSTIBLE_CHOICES)
    transmision = models.CharField(max_length=15, choices=TRANSMISION_CHOICES)
    puertas = models.SmallIntegerField(choices=[(2,2), (3,3), (4,4), (5,5)])
    motor = models.CharField(max_length=50)
    traccion = models.CharField(max_length=15, choices=TRACCION_CHOICES, null=True, blank=True)
    numero_serie_motor = models.CharField(max_length=100)
    procedencia = models.CharField(max_length=20, choices=PROCEDENCIA_CHOICES, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Validación de unicidad de patente 
        if self.patente:
            # Buscamos otros vehículos con la misma patente, excluyendo el objeto actual (si ya tiene PK)
            queryset = Vehiculo.objects.filter(patente=self.patente)
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            
            if queryset.exists():
                raise ValidationError({"patente": "Esta patente ya está registrada en otro vehículo."})
            
        if not self.vin or not self.vin.strip():
            raise ValidationError({"vin": "El VIN es obligatorio para todos los vehículos."})
            
        #  Validación para USADOS
        if self.condicion_vehiculo == 'usado':
            if not self.patente:
                raise ValidationError({"patente": "La patente es obligatoria para vehículos usados."})
            if (self.kilometraje or 0) <= 0:
                raise ValidationError({"kilometraje": "El kilometraje debe ser mayor a 0 para usados."})
            
            if not self.procedencia:
                raise ValidationError({"procedencia": "La procedencia es obligatoria para usados."})
            if not self.numero_serie_motor:
                raise ValidationError({"numero_serie_motor": "El número de serie del motor es obligatorio."})
        
        #  Validación para 0KM
        if self.condicion_vehiculo == '0km':
            if self.patente and self.estado != 'vendido':
                raise ValidationError({"patente": "Un vehículo 0km no debe tener patente asignada."})
           
            if (self.kilometraje or 0) > 500:
                raise ValidationError({"kilometraje": "Un vehículo 0km no puede tener más de 500 km."})
        
        if self.entregado:
            if self.condicion_vehiculo == '0km' and not self.patente:
                raise ValidationError({'patente': 'Para marcar como entregado un 0km debe tener patente asignada.'})
    
    def save(self, *args, **kwargs):
        if self.kilometraje is None:
            self.kilometraje = 0
        
        if not self.pk:
            self.fecha_cambio_estado = timezone.now()
        else:
            original = Vehiculo.all_objects.filter(pk=self.pk).first()
            if original and original.estado != self.estado:
                self.fecha_cambio_estado = timezone.now()
        
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
    
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        raise ValidationError("No está permitido eliminar vehículos físicamente. Use la desactivación.")

    # Método de borrado lógico
    def soft_delete(self):
        if self.estado in ['reservado', 'vendido']:
            raise ValidationError(f"No es posible desactivar un vehículo {self.estado}.")
        self.activo = False
        self.save()

    # Manager personalizado para filtrar automáticamente solo los activos
    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(activo=True)

    objects = ActiveManager() # por defecto
    all_objects = models.Manager() # Para acceder a todo (incluyendo los inactivos)
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.patente or self.vin}"
    

#Fotografia =======================================================================================

def validate_file_size(value):
    limit = 5 * 1024 * 1024  # 5 MB
    if value.size > limit:
        raise ValidationError("La imagen es muy pesada. Máximo 5 MB por archivo.")

class Fotografia_Vehiculo(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='fotos')
    archivo = models.ImageField(upload_to='vehiculos/')
   
    nombre_original = models.CharField(max_length=255, blank=True, null=True)
    es_portada = models.BooleanField(default=False)
    
    tamano_bytes = models.IntegerField(editable=False) 
    mime_type = models.CharField(max_length=50, editable=False)
    orden = models.PositiveIntegerField(default=1)
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vehiculo', 'orden'], name='unique_orden_por_vehiculo'),
        ]

    def clean(self):
        # Validación de formato
        if self.archivo:
            if not self.archivo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                raise ValidationError({'archivo': 'Solo se permiten formatos JPG, PNG o WEBP.'})

        # Validación de límite de 10 fotos
        if self.pk is None and self.vehiculo_id:
            fotos_actuales = Fotografia_Vehiculo.objects.filter(vehiculo=self.vehiculo).count()
            if fotos_actuales >= 10:
                raise ValidationError("Un vehículo no puede tener más de 10 fotografías.")
        
        if self.orden is not None and (self.orden < 1 or self.orden > 10):
            raise ValidationError({'orden': 'El orden debe estar entre 1 y 10.'})

    def save(self, *args, **kwargs):
        #   metadatos
        if self.archivo:
            # Calculo tamaño
            self.tamano_bytes = self.archivo.size
            # Calculo MIME type
            mime, _ = mimetypes.guess_type(self.archivo.name)
            self.mime_type = mime or 'image/jpeg'
            # nombre original si está vacío
            if not self.nombre_original:
                self.nombre_original = self.archivo.name

        # Asignar orden automáticamente si es nuevo
        if not self.pk and (self.orden is None or self.orden == 1):
            max_orden = Fotografia_Vehiculo.objects.filter(vehiculo=self.vehiculo).aggregate(
                models.Max('orden')
            )['orden__max'] or 0
            self.orden = max_orden + 1

      
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Foto de {self.vehiculo} - Orden {self.orden}"
    

 # Taller =====================================================================

class Taller(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=150, blank=True)
    estado = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    

# VehiculoUsado =====================================================================

class VehiculoUsado(models.Model):
    ESTADO_COMPONENTE_CHOICES = [
        ('bueno', 'Bueno'), ('regular', 'Regular'), ('malo', 'Malo')
    ]

    vehiculo = models.OneToOneField(
        Vehiculo, on_delete=models.PROTECT, related_name='vehiculo_usado'
    )

    taller = models.ForeignKey(
        Taller, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='evaluaciones'
    )
    
    usuario_autoriza = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='vehiculos_autorizados'
    )
    
    precio_info_auto = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    porcentaje_deduccion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    precio_tasacion_final = models.DecimalField(max_digits=14, decimal_places=2)

    estado_cubierta = models.CharField(max_length=10, choices=ESTADO_COMPONENTE_CHOICES, null=True, blank=True)
    estado_motor = models.CharField(max_length=10, choices=ESTADO_COMPONENTE_CHOICES, null=True, blank=True)
    estado_chapa_pintura = models.CharField(max_length=10, choices=ESTADO_COMPONENTE_CHOICES, null=True, blank=True)
    estado_interior = models.CharField(max_length=10, choices=ESTADO_COMPONENTE_CHOICES, null=True, blank=True)

    fecha_evaluacion = models.DateField(null=True, blank=True)
    fecha_ingreso = models.DateField()
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(porcentaje_deduccion__isnull=True) |
                      models.Q(porcentaje_deduccion__gte=15.00, porcentaje_deduccion__lte=20.00),
                name='check_porcentaje_deduccion_rango'
            ),
            models.CheckConstraint(
                check=models.Q(precio_tasacion_final__gt=0),
                name='check_precio_tasacion_positivo'
            ),
        ]

    def clean(self):
        if self.vehiculo_id and self.vehiculo.condicion_vehiculo != 'usado':
            raise ValidationError({'vehiculo': 'Solo se pueden registrar vehículos con condición usado.'})
        
        if self.precio_tasacion_final is not None and self.precio_tasacion_final <= 0:
            raise ValidationError({'precio_tasacion_final': 'El precio de tasación debe ser mayor a cero.'})
        
        hoy = datetime.date.today()

        if self.fecha_ingreso and self.fecha_ingreso > hoy:
            raise ValidationError({'fecha_ingreso': 'La fecha de ingreso no puede ser futura.'})
        if self.fecha_ingreso and (hoy - self.fecha_ingreso).days > 30:
            raise ValidationError({'fecha_ingreso': 'La fecha de ingreso no puede ser anterior a 30 días.'})

        if self.fecha_evaluacion:
            if self.fecha_evaluacion > hoy:
                raise ValidationError({'fecha_evaluacion': 'La fecha de evaluación no puede ser futura.'})
            if (hoy - self.fecha_evaluacion).days > 30:
                raise ValidationError({'fecha_evaluacion': 'La fecha de evaluación no puede ser anterior a 30 días.'})
            if self.fecha_ingreso and self.fecha_evaluacion > self.fecha_ingreso:
                raise ValidationError({'fecha_evaluacion': 'La fecha de evaluación no puede ser posterior a la fecha de ingreso.'})


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.full_clean()
        super().save(*args, **kwargs)
        # Actualiza precio_costo en Vehiculo solo al crear
        if is_new:
            Vehiculo.all_objects.filter(pk=self.vehiculo_id).update(
                precio_costo=self.precio_tasacion_final
            )

    def __str__(self):
        return f"Usado: {self.vehiculo}"


# TrasladoVehiculo ==================================================================

class TrasladoVehiculo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'), ('completado', 'Completado'), ('cancelado', 'Cancelado')
    ]

    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name='traslados'
    )
    sucursal_origen = models.ForeignKey(
        'sucursal.Sucursal', on_delete=models.PROTECT, related_name='traslados_salida'
    )
    sucursal_destino = models.ForeignKey(
        'sucursal.Sucursal', on_delete=models.PROTECT, related_name='traslados_entrada'
    )
    usuario_autoriza = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='traslados_autorizados'
    )
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='traslados_registrados'
    )

    costo_traslado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    fecha_traslado = models.DateField()
    motivo = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def clean(self):
    if not self.pk and self.vehiculo_id:
        if self.vehiculo.estado == 'vendido':
            raise ValidationError({'vehiculo': 'No se puede trasladar un vehículo vendido.'})
        if self.sucursal_origen_id and self.vehiculo.sucursal_id != self.sucursal_origen_id:
            raise ValidationError({'sucursal_origen': 'La sucursal origen no coincide con la sucursal actual del vehículo.'})
        
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Traslado {self.vehiculo} | {self.sucursal_origen} → {self.sucursal_destino}"
    
   