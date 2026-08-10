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

        if original and original.observaciones:
            if not (self.observaciones or '').startswith(original.observaciones):
                raise ValidationError({
                    'observaciones': 'No se puede modificar ni eliminar el texto de observaciones ya registrado. Solo se puede agregar texto al final.'
                })
            
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
            self.valor_vehiculo_usado = self.vehiculo_usado_entregado.precio_costo or 0
        else:
            self.valor_vehiculo_usado = 0

        self.precio_final = (self.precio_original or 0) - (self.descuento_aplicado or 0) - (self.valor_vehiculo_usado or 0)

        if not skip_validation:
            self.full_clean(exclude=['precio_final', 'precio_original', 'valor_vehiculo_usado'])
        
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
        return f"#{self.pk} | {self.tipo_pago} - ${self.monto} | Op {self.operacion.id} | {self.fecha_registro.strftime('%d/%m/%Y') if self.fecha_registro else ''}"

     
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
    cliente = models.ForeignKey(
    'clientes.Cliente', on_delete=models.PROTECT, related_name='anticipos',
    null=True, blank=True  # cambiar cuando sergio tenga listo clientes.-
)
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='anticipos_registrados'
    )
    operacion_aplicado = models.ForeignKey(
        OperacionVenta, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='anticipos'
    )
    
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
    


# ===================== TITULO DE CREDITO =====================

class TituloCredito(models.Model):
    TIPO_CHOICES = [
        ('cheque', 'Cheque'),
        ('pagare', 'Pagaré'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('habilitado', 'Habilitado'),
        ('vencido', 'Vencido'),
        ('cobrado', 'Cobrado'),
        ('rechazado', 'Rechazado'),
        ('en_gestion', 'En Gestión'),
    ]
    FORMA_ACREDITACION_CHOICES = [
        ('ventanilla', 'Ventanilla'),
        ('deposito', 'Depósito'),
    ]
    PLAZO_CHOICES = [(0, '0'), (30, '30'), (60, '60'), (90, '90')]


    forma_pago = models.OneToOneField(
        'FormaPago', on_delete=models.PROTECT,
        null=True, blank=True, related_name='titulo_credito'
    )
    anticipo = models.OneToOneField(
        'Anticipo', on_delete=models.PROTECT,
        null=True, blank=True, related_name='titulo_credito'
    )
    documento_origen = models.ForeignKey(
        'self', on_delete=models.PROTECT,
        null=True, blank=True, related_name='renovaciones',
        help_text='Dejar vacío salvo que este título reemplace a otro rechazado o en gestión.'
    )

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero_documento = models.CharField(max_length=20)
    banco_emisor = models.CharField(max_length=100, null=True, blank=True)
    titular = models.CharField(max_length=150, null=True, blank=True)

    plazo_dias = models.IntegerField(choices=PLAZO_CHOICES, null=True, blank=True)  
    fecha_vencimiento_manual = models.DateField(
        null=True, blank=True,
        help_text="Solo para pagarés. Fecha de vencimiento acordada, independiente de plazos fijos."
    )
    fecha_recepcion = models.DateField()
    fecha_cobro = models.DateField(blank=True)
    fecha_acreditacion = models.DateField(null=True, blank=True)
    forma_acreditacion = models.CharField(
        max_length=15, choices=FORMA_ACREDITACION_CHOICES,
        null=True, blank=True
    )

    monto = models.DecimalField(max_digits=14, decimal_places=2)
    interes_mora = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['numero_documento', 'banco_emisor'],
                condition=models.Q(banco_emisor__isnull=False),
                name='unique_numero_banco_emisor'
            ),
            models.CheckConstraint(
                check=models.Q(monto__gt=0),
                name='check_monto_titulo_positivo'
            ),
        ]

    def clean(self):
        if self.tipo == 'cheque':
            if self.plazo_dias is None:
                raise ValidationError({'plazo_dias': 'El plazo en días es obligatorio para cheques.'})
            if self.fecha_vencimiento_manual:
                raise ValidationError({'fecha_vencimiento_manual': 'Este campo no aplica para cheques.'})

        if self.tipo == 'pagare':
            if not self.fecha_vencimiento_manual:
                raise ValidationError({'fecha_vencimiento_manual': 'Debe indicar la fecha de vencimiento del pagaré.'})
            if self.plazo_dias:
                raise ValidationError({'plazo_dias': 'Este campo no aplica para pagarés, use fecha de vencimiento manual.'})

        # banco_emisor obligatorio para cheques
        if self.tipo == 'cheque' and not self.banco_emisor:
            raise ValidationError({'banco_emisor': 'El banco emisor es obligatorio para cheques.'})

        # interes_mora solo para pagarés
        if self.tipo == 'cheque' and self.interes_mora and self.interes_mora > 0:
            raise ValidationError({'interes_mora': 'El interés de mora solo aplica para pagarés.'})

        # forma_pago y anticipo no pueden ser ambos null ni ambos completos
        if not self.forma_pago_id and not self.anticipo_id:
            raise ValidationError('Debe referenciar una forma de pago o un anticipo.')
        if self.forma_pago_id and self.anticipo_id:
            raise ValidationError('No puede referenciar una forma de pago y un anticipo al mismo tiempo.')

        # observaciones obligatorio cuando rechazado o en_gestion
        if self.estado in ['rechazado', 'en_gestion'] and not self.observaciones:
            raise ValidationError({'observaciones': 'Debe indicar el motivo cuando el estado es rechazado o en gestión.'})

        # fecha_cobro máximo 90 días desde recepción
        if self.fecha_recepcion and self.fecha_cobro:
            delta = (self.fecha_cobro - self.fecha_recepcion).days
            if delta > 90:
                raise ValidationError({'fecha_cobro': 'La fecha de cobro no puede superar los 90 días desde la recepción.'})

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)  # ← faltaba esto

        if self.tipo == 'cheque' and self.fecha_recepcion and self.plazo_dias is not None:
            from datetime import timedelta
            self.fecha_cobro = self.fecha_recepcion + timedelta(days=self.plazo_dias)
        elif self.tipo == 'pagare' and self.fecha_vencimiento_manual:
            self.fecha_cobro = self.fecha_vencimiento_manual

        if not skip_validation: 
            self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.tipo} #{self.numero_documento} - ${self.monto} ({self.estado})"


# ===================== REGISTRO DE COBRO =====================

class RegistroCobro(models.Model):
    FORMA_COBRO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
        ('pagare', 'Pagaré'),
    ]
    FORMA_ACREDITACION_CHOICES = [
        ('ventanilla', 'Ventanilla'),
        ('deposito', 'Depósito'),
    ]

    titulo = models.ForeignKey(
        TituloCredito, on_delete=models.PROTECT, related_name='registros_cobro'
    )
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='cobros_registrados'
    )

    fecha_pago_real = models.DateField()
    monto_pagado = models.DecimalField(max_digits=14, decimal_places=2)
    pago_con_mora = models.BooleanField(default=False)
    monto_mora_pagado = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    forma_cobro = models.CharField(max_length=15, choices=FORMA_COBRO_CHOICES)
    forma_acreditacion_cheque = models.CharField(
        max_length=15, choices=FORMA_ACREDITACION_CHOICES,
        null=True, blank=True,
        help_text="Solo para cheques: cómo se hizo efectivo (ventanilla o depósito)."
    )
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(monto_pagado__gt=0),
                name='check_monto_pagado_positivo'
            ),
        ]
    def clean(self):
        if self.pago_con_mora and self.titulo.tipo != 'pagare':
            raise ValidationError({'pago_con_mora': 'El pago con mora solo aplica para pagarés.'})

        if self.monto_mora_pagado > 0 and self.titulo.tipo != 'pagare':
            raise ValidationError({'monto_mora_pagado': 'El monto de mora solo aplica para pagarés.'})

        if self.titulo.tipo == 'cheque' and self.forma_cobro != 'cheque':
            raise ValidationError({
                'forma_cobro': 'Para un cheque, la forma de cobro debe ser "cheque".'
            })

        if self.titulo.tipo == 'cheque' and not self.forma_acreditacion_cheque:
            raise ValidationError({
                'forma_acreditacion_cheque': 'Debe indicar si el cheque se cobró por ventanilla o depósito.'
            })

        if self.titulo.tipo != 'cheque' and self.forma_acreditacion_cheque:
            raise ValidationError({
                'forma_acreditacion_cheque': 'Este campo solo aplica para cheques.'
            })

    def save(self, *args, **kwargs):
        if self.titulo.tipo == 'cheque':
            self.forma_cobro = 'cheque'

        self.full_clean()
        super().save(*args, **kwargs)

        self.titulo.estado = 'cobrado'
        self.titulo.fecha_acreditacion = self.fecha_pago_real
        if self.titulo.tipo == 'cheque':
            self.titulo.forma_acreditacion = self.forma_acreditacion_cheque
        self.titulo.save(skip_validation=True)