from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError as DjangoValidationError

#============================OPERACION DE VENTA ===========================================

class OperacionVenta(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    # Relaciones
    sucursal = models.ForeignKey('sucursal.Sucursal', on_delete=models.PROTECT, related_name='operaciones')
    # TODO: Cambiar a 'clientes.Cliente' cuando el módulo de sergiio esté listo
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='operaciones_titular', null=True, blank=True)
    cliente_cotitular = models.ForeignKey('clientes.Cliente', null=True, blank=True, on_delete=models.PROTECT, related_name='operaciones_cotitular')
    
    vehiculo_vendido = models.ForeignKey('inventario.Vehiculo', on_delete=models.PROTECT, related_name='operaciones_venta')
    vehiculo_usado_entregado = models.ForeignKey('inventario.Vehiculo', on_delete=models.PROTECT, related_name='operaciones_compra', null=True, blank=True)
    
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ventas_iniciadas')
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='ventas_confirmadas')
    anticipo = models.ForeignKey('ventas.Anticipo', on_delete=models.SET_NULL, null=True, blank=True, related_name='operacion_aplicada')

    # Datos comerciales
    fecha_operacion = models.DateField(default=timezone.now)
    precio_original = models.DecimalField(max_digits=14, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    precio_final = models.DecimalField(max_digits=14, decimal_places=2)
    valor_vehiculo_usado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, default=0)
    
    
    # Gestión
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='borrador')
    numero_boleto = models.CharField(max_length=20, null=True, blank=True)
    ruta_boleto_pdf = models.CharField(max_length=500, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    
    # Fechas
    fecha_cambio_estado = models.DateTimeField(null=True, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        original = OperacionVenta.objects.filter(pk=self.pk).first() if self.pk else None

        if self.cliente_cotitular and self.cliente_cotitular == self.cliente:
            raise ValidationError({'cliente_cotitular': 'El cotitular no puede ser el mismo que el titular.'})

        if self.estado == 'cancelada' and not self.observaciones:
            raise ValidationError({'observaciones': 'Debe indicar el motivo de la cancelación.'})

        if original and original.estado != 'borrador':
            if self.precio_original != original.precio_original:
                raise ValidationError({'precio_original': 'No se puede modificar el precio una vez confirmada la operación.'})

        if original and original.estado == 'borrador' and self.estado == 'confirmada':
            raise ValidationError({'estado': 'No se puede confirmar una operación directamente. Use la acción confirmar.'})

        if original and original.estado == 'confirmada' and self.estado == 'borrador':
            raise ValidationError({'estado': 'No se puede revertir una operación confirmada a borrador.'})

        if self.anticipo and self.vehiculo_vendido and self.anticipo.vehiculo != self.vehiculo_vendido:
            raise ValidationError({'anticipo': 'El anticipo no corresponde al vehículo seleccionado.'})

        if not self.pk and self.vehiculo_vendido_id:
            operaciones_activas = OperacionVenta.objects.filter(
                vehiculo_vendido=self.vehiculo_vendido,
                estado__in=['borrador', 'confirmada']
            )
            if operaciones_activas.exists():
                raise ValidationError({'vehiculo_vendido': 'Ya existe una operación activa para este vehículo.'})

        hoy = datetime.date.today()
        if self.fecha_operacion:
            fecha_op = self.fecha_operacion.date() if hasattr(self.fecha_operacion, 'date') else self.fecha_operacion
            if fecha_op > hoy:
                raise ValidationError({'fecha_operacion': 'La fecha de operación no puede ser futura.'})
            if (hoy - fecha_op).days > 30:
                raise ValidationError({'fecha_operacion': 'La fecha de operación no puede ser anterior a 30 días.'})

        if self.vehiculo_vendido_id:
            from inventario.models import Vehiculo
            vehiculo = Vehiculo.all_objects.get(pk=self.vehiculo_vendido_id)
            if vehiculo.estado == 'vendido':
                raise ValidationError({'vehiculo_vendido': 'No se puede crear una operación para un vehículo ya vendido.'})

        if self.valor_vehiculo_usado and self.precio_original:
            saldo = self.precio_original - (self.descuento_aplicado or 0)
            if self.valor_vehiculo_usado > saldo:
                raise ValidationError({
                    'vehiculo_usado_entregado': 'El valor del vehículo usado no puede superar el precio a pagar.'
                })
        
    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        
        if self.vehiculo_vendido:
            self.precio_original = self.vehiculo_vendido.precio
        if self.vehiculo_usado_entregado:
            self.valor_vehiculo_usado = self.vehiculo_usado_entregado.precio_costo

        self.precio_final = (self.precio_original or 0) - (self.descuento_aplicado or 0) - (self.valor_vehiculo_usado or 0)

        if not skip_validation:
            self.full_clean(exclude=['precio_final'])
        
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Op {self.id} - Vehículo: {self.vehiculo_vendido.patente or self.vehiculo_vendido.vin}"

#==============FORMA DE PAGO ====================================================

class FormaPago(models.Model):
    TIPO_PAGO_CHOICES = [
            ('efectivo', 'Efectivo'),
            ('cheque', 'Cheque'),
            ('pagare', 'Pagaré'),
            ('financiamiento_externo', 'Financiamiento Externo'),
            ('financiamiento_interno', 'Financiamiento Interno'),
            ('dolares', 'Dólares'),
        ]

    operacion = models.ForeignKey(OperacionVenta, on_delete=models.CASCADE, related_name='formas_pago')
    tipo_pago = models.CharField(max_length=30, choices=TIPO_PAGO_CHOICES)
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    cotizacion_dolar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(monto__gt=0), name='check_monto_forma_pago_positivo')
        ]

    def clean(self):
        if self.tipo_pago == 'dolares' and not self.cotizacion_dolar:
            raise ValidationError({'cotizacion_dolar': 'La cotización del dólar es obligatoria cuando el tipo de pago es dólares.'})
        if self.tipo_pago != 'dolares' and self.cotizacion_dolar:
            raise ValidationError({'cotizacion_dolar': 'La cotización del dólar solo aplica cuando el tipo de pago es dólares.'})
        
        
    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo_pago} - ${self.monto} | Op {self.operacion.id}"
    
#======================ANTICIPO====================================================

class Anticipo(models.Model):
    FORMA_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aplicado', 'Aplicado'),
        ('devuelto', 'Devuelto'),
        ('retenido', 'Retenido'),
    ]

    vehiculo = models.ForeignKey(
        'inventario.Vehiculo', on_delete=models.PROTECT, related_name='anticipos'
    )
    # cambiar a 'clientes.Cliente' cuando Sergio termine ===============================
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT, related_name='anticipos'
    )
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='anticipos_registrados'
    )
    operacion_aplicado = models.ForeignKey(
        OperacionVenta, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='anticipos'
    )
    # titulo = models.ForeignKey(
    #     'ventas.TituloCredito', on_delete=models.SET_NULL,
    #     null=True, blank=True, related_name='anticipo'
    # )

    monto = models.DecimalField(max_digits=14, decimal_places=2)
    forma_pago = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES)
    fecha_anticipo = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(monto__gt=0), name='check_monto_anticipo_positivo')
        ]

    def clean(self):
        if self.estado in ['devuelto', 'retenido'] and not self.observaciones:
            raise ValidationError({'observaciones': 'Debe indicar el motivo cuando el estado es devuelto o retenido.'})

        if self.monto is not None and self.monto <= 0:
            raise ValidationError({'monto': 'El monto debe ser mayor a cero.'})
        hoy = datetime.date.today()

        if self.fecha_anticipo:
            if self.fecha_anticipo > hoy:
                raise ValidationError({'fecha_anticipo': 'La fecha del anticipo no puede ser futura.'})
            if (hoy - self.fecha_anticipo).days > 30:
                raise ValidationError({'fecha_anticipo': 'La fecha del anticipo no puede ser anterior a 30 días.'})

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
        super().save(*args, **kwargs)
        # Al crear el anticipo, cambia el vehículo a reservado
        if is_new:
            self.vehiculo.estado = 'reservado'
            self.vehiculo.save(skip_validation=True)

    def __str__(self):
        return f"Anticipo ${self.monto} - {self.vehiculo}"