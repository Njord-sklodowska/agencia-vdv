from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.core.validators import RegexValidator

numero_cheque_validator = RegexValidator(
    regex=r'^\d{8}$',
    message='El número de cheque debe tener 8 dígitos numéricos.',
    code='invalid_numero_cheque'
)

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

    # validaciones
    def clean(self):
        original = OperacionVenta.objects.filter(pk=self.pk).first() if self.pk else None

        if self.cliente_cotitular and self.cliente_cotitular == self.cliente:
            raise ValidationError({'cliente_cotitular': 'El cotitular no puede ser el mismo que el titular.'})

        if self.vehiculo_vendido and self.vehiculo_usado_entregado and self.vehiculo_vendido == self.vehiculo_usado_entregado:
            raise ValidationError({'vehiculo_usado_entregado': 'El vehículo usado entregado no puede ser el mismo que el vehículo que se está vendiendo.'})

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

        if self.descuento_aplicado and self.precio_original and self.descuento_aplicado > self.precio_original:
            raise ValidationError({'descuento_aplicado': 'El descuento no puede superar el precio original.'})

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

        # precio_original queda fijo como precio SOLO al crear la operación.
        # Al ser editado posteriormente no se vuelve a tomar del vehiculo, para no pisar
        # silenciosamente el precio acordado si el vehículo cambia de precio después.
        if self.pk is None and self.vehiculo_vendido:
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
       models.CheckConstraint(condition=models.Q(monto__gt=0), name='check_monto_forma_pago_positivo')]

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

    #relaciones
    vehiculo = models.ForeignKey(
        'inventario.Vehiculo', on_delete=models.PROTECT, related_name='anticipos')
    cliente = models.ForeignKey(
    'clientes.Cliente', on_delete=models.PROTECT, related_name='anticipos',null=True, blank=True)
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='anticipos_registrados')
    operacion_aplicado = models.ForeignKey(
        OperacionVenta, on_delete=models.SET_NULL,null=True, blank=True, related_name='anticipos')

    # datos generales    
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    forma_pago = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)

    #fechas
    fecha_anticipo = models.DateField()
    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(monto__gt=0), name='check_monto_anticipo_positivo')
        ]

    def clean(self):
        if self.estado in ['devuelto', 'retenido'] and not self.observaciones:
            raise ValidationError({'observaciones': 'Debe indicar el motivo cuando el estado es devuelto o retenido.'})

        if self.monto is not None and self.monto <= 0:
            raise ValidationError({'monto': 'El monto debe ser mayor a cero.'})

        if not self.pk and self.vehiculo_id and self.vehiculo.estado != 'en_stock':
            raise ValidationError({'vehiculo': f'No se puede registrar un anticipo para un vehículo en estado "{self.vehiculo.estado}".'})

        hoy = datetime.date.today()
        
        # Validar que la fecha del anticipo no sea en el futuro
        if self.fecha_anticipo and self.fecha_anticipo > hoy:
            raise ValidationError({'fecha_anticipo': 'La fecha del anticipo no puede ser futura.'})

        # Validar que no sea mayor a 30 días en el pasado
        if self.fecha_anticipo and (hoy - self.fecha_anticipo).days > 30:
            raise ValidationError({'fecha_anticipo': 'La fecha del anticipo no puede ser anterior a 30 días.'})
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        estado_anterior = None
        
        if not is_new:
            # Obtenemos el estado anterior de la base de datos para comparar
            estado_anterior = Anticipo.objects.filter(pk=self.pk).values_list('estado', flat=True).first()

        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
            
        super().save(*args, **kwargs)
        
        # Al crear el anticipo, cambia el vehículo a reservado
        if is_new:
            self.vehiculo.estado = 'reservado'
            self.vehiculo.save(skip_validation=True)
        # Si pasa a devuelto o retenido, liberamos el vehículo a en_stock
        elif estado_anterior != self.estado and self.estado in ['devuelto', 'retenido']:
            if self.vehiculo.estado == 'reservado':
                self.vehiculo.estado = 'en_stock'
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
    #datos del titulo de credito
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero_documento = models.CharField(max_length=20)
    banco_emisor = models.CharField(max_length=100, null=True, blank=True)
    titular = models.CharField(max_length=150, null=True, blank=True)
    plazo_dias = models.IntegerField(choices=PLAZO_CHOICES, null=True, blank=True)
    monto = models.DecimalField(max_digits=14, decimal_places=2)
    interes_mora = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)  
    
    #fechas
    fecha_vencimiento_manual = models.DateField(
        null=True, blank=True,
        help_text="Obligatoria para pagarés. Opcional para cheques cuando hay plazos."
    )
    
    fecha_recepcion = models.DateField()
    fecha_cobro = models.DateField(blank=True)
    fecha_acreditacion = models.DateField(null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    forma_acreditacion = models.CharField(
        max_length=15, choices=FORMA_ACREDITACION_CHOICES,
        null=True, blank=True
    )
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name='check_monto_titulo_positivo'),
        ]

    def clean(self):
        if self.tipo == 'cheque':
            if self.plazo_dias is None and not self.fecha_vencimiento_manual:
                raise ValidationError('Debe indicar el plazo en días o una fecha de vencimiento manual para el cheque.')
            if self.plazo_dias is not None and self.fecha_vencimiento_manual:
                raise ValidationError('No puede indicar plazo_dias y fecha_vencimiento_manual al mismo tiempo. Use solo uno.')

        if self.tipo == 'pagare':
            if not self.fecha_vencimiento_manual:
                raise ValidationError({'fecha_vencimiento_manual': 'Debe indicar la fecha de vencimiento del pagaré.'})
            if self.plazo_dias:
                raise ValidationError({'plazo_dias': 'Este campo no aplica para pagarés, use fecha de vencimiento manual.'})

            if not self.titular:
                raise ValidationError({'titular': 'El titular es obligatorio para pagarés.'})

        if self.tipo == 'cheque' and not self.banco_emisor:
            raise ValidationError({'banco_emisor': 'El banco emisor es obligatorio para cheques.'})

        if self.tipo == 'cheque' and self.numero_documento:
            try:
                numero_cheque_validator(self.numero_documento)
            except ValidationError as e:
                raise ValidationError({'numero_documento': e.messages})

        if self.tipo == 'cheque' and self.interes_mora and self.interes_mora > 0:
            raise ValidationError({'interes_mora': 'El interés de mora solo aplica para pagarés.'})

        if not self.forma_pago_id and not self.anticipo_id:
            raise ValidationError('Debe referenciar una forma de pago o un anticipo.')
        if self.forma_pago_id and self.anticipo_id:
            raise ValidationError('No puede referenciar una forma de pago y un anticipo al mismo tiempo.')
        
    # El tipo del título debe coincidir con el tipo_pago de la forma de pago referenciada
        if self.forma_pago_id and self.forma_pago.tipo_pago != self.tipo:
            raise ValidationError({
                'tipo': f'El tipo de título ({self.tipo}) no coincide con el tipo de la forma de pago referenciada ({self.forma_pago.tipo_pago}).'
            })

    # El monto del título debe coincidir con el de la forma de pago o anticipo que referencia
        if self.forma_pago_id and self.monto != self.forma_pago.monto:
            raise ValidationError({
                'monto': f'El monto (${self.monto}) debe coincidir con el de la forma de pago (${self.forma_pago.monto}).'
            })
        if self.anticipo_id and self.monto != self.anticipo.monto:
            raise ValidationError({
                'monto': f'El monto (${self.monto}) debe coincidir con el del anticipo (${self.anticipo.monto}).'
            })

        if self.estado in ['rechazado', 'en_gestion'] and not self.observaciones:
            raise ValidationError({'observaciones': 'Debe indicar el motivo cuando el estado es rechazado o en gestión.'})

        hoy = datetime.date.today()
        if self.fecha_recepcion and self.fecha_recepcion > hoy:
            raise ValidationError({'fecha_recepcion': 'La fecha de recepción no puede ser futura.'})

        if self.fecha_recepcion and self.fecha_cobro:
            delta = (self.fecha_cobro - self.fecha_recepcion).days
            if delta > 90:
                raise ValidationError({'fecha_cobro': 'La fecha de cobro no puede superar los 90 días desde la recepción.'})

        # Unicidad numero_documento + banco_emisor 
        if self.banco_emisor:
            queryset = TituloCredito.objects.filter(
                numero_documento=self.numero_documento,
                banco_emisor=self.banco_emisor,
            )
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError({'numero_documento': 'Ya existe un título con este número de documento para el mismo banco emisor.'})

        if self.tipo == 'pagare' and self.titular:
            queryset = TituloCredito.objects.filter(
                tipo='pagare',
                numero_documento=self.numero_documento,
                titular=self.titular,
            )
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            if queryset.exists():
                raise ValidationError({'numero_documento': 'Ya existe un pagaré con este número de documento para el mismo titular.'})

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)

        if self.fecha_vencimiento_manual:
            self.fecha_cobro = self.fecha_vencimiento_manual
        elif self.tipo == 'cheque' and self.fecha_recepcion and self.plazo_dias is not None:
            from datetime import timedelta
            self.fecha_cobro = self.fecha_recepcion + timedelta(days=self.plazo_dias)

        if not skip_validation:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} #{self.numero_documento} - ${self.monto} ({self.estado})"


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
    # datos del pago
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
                condition=models.Q(monto_pagado__gt=0),
                name='check_monto_pagado_positivo'
            ),
        ]

    def clean(self):
        hoy = datetime.date.today()

        # No se puede registrar un cobro sobre un título ya cobrado (evita duplicar el cobro,
        # sin importar si se llega desde la acción registrar_cobro/ o el POST directo de este endpoint).
        if not self.pk and self.titulo_id:
            titulo = self.titulo
            if titulo.estado == 'cobrado':
                raise ValidationError('Este título ya fue cobrado. No se puede registrar un cobro duplicado.')

        if self.fecha_pago_real and self.fecha_pago_real > hoy:
            raise ValidationError({'fecha_pago_real': 'La fecha de pago no puede ser futura.'})

        if self.pago_con_mora and (self.titulo.tipo != 'pagare' or self.titulo.estado != 'vencido'):
            raise ValidationError({'pago_con_mora': 'El pago con mora solo aplica a pagarés en estado vencido.'})
        
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
       
        with transaction.atomic():
            super().save(*args, **kwargs)

            self.titulo.estado = 'cobrado'
            self.titulo.fecha_acreditacion = self.fecha_pago_real
            if self.titulo.tipo == 'cheque':
                self.titulo.forma_acreditacion = self.forma_acreditacion_cheque
            self.titulo.save(skip_validation=True)


# =========================== ENTIDAD FINANCIERA ===========================

class EntidadFinanciera(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')

    fecha_alta = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


# ===================== FINANCIAMIENTO EXTERNO ============================

class FinanciamientoExterno(models.Model):
    """ La concesionaria no gestiona la deuda ni el
    cobro de este crédito. Solo deja constancia de que el vehículo fue
    pagado mediante financiamiento externo """

    operacion = models.ForeignKey(
        OperacionVenta, on_delete=models.PROTECT, related_name='financiamientos_externos'
    )
    forma_pago = models.OneToOneField(
        'FormaPago', on_delete=models.PROTECT, related_name='financiamiento_externo'
    )
    entidad = models.ForeignKey(
        EntidadFinanciera, on_delete=models.PROTECT, related_name='financiamientos'
    )

    monto_aprobado = models.DecimalField(max_digits=14, decimal_places=2)
    numero_credito = models.CharField(max_length=50, null=True, blank=True)
    fecha_aprobacion = models.DateField(null=True, blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto_aprobado__gt=0),
                name='check_monto_aprobado_positivo'
            ),
        ]

    def clean(self):
        if self.forma_pago_id and self.forma_pago.tipo_pago != 'financiamiento_externo':
            raise ValidationError({
                'forma_pago': 'La forma de pago debe ser de tipo "financiamiento_externo".'
            })

        if self.operacion_id and self.forma_pago_id and self.forma_pago.operacion_id != self.operacion_id:
            raise ValidationError({
                'forma_pago': 'La forma de pago no corresponde a la operación seleccionada.'
            })

        hoy = datetime.date.today()
        if self.fecha_aprobacion and self.fecha_aprobacion > hoy:
            raise ValidationError({'fecha_aprobacion': 'La fecha de aprobación no puede ser futura.'})

    def save(self, *args, **kwargs):
        omitir_validation = kwargs.pop('omitir_validation', False)
        if not omitir_validation:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Financiamiento {self.entidad} - ${self.monto_aprobado} (Op {self.operacion_id})"


# ================================ CREDITO INTERNO ======================================

class CreditoInterno(models.Model):
    """Financiamiento propio de la concesionaria, pagado en cuotas.simplifiqué: no hay proceso automático diario de verificación de mora ni alertas; el estado se actualiza cuando
    el administrativo registra el pago de cada cuota."""
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('en_mora', 'En Mora'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    operacion = models.ForeignKey(
        OperacionVenta, on_delete=models.PROTECT, related_name='creditos_internos'
    )
    forma_pago = models.OneToOneField(
        'FormaPago', on_delete=models.PROTECT, related_name='credito_interno'
    )

    monto_financiado = models.DecimalField(max_digits=14, decimal_places=2)
    cantidad_cuotas = models.PositiveIntegerField()
    tasa_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    monto_cuota = models.DecimalField(max_digits=14, decimal_places=2, editable=False)
    monto_total = models.DecimalField(max_digits=14, decimal_places=2, editable=False)

    fecha_primera_cuota = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activo')
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad_cuotas__gt=0),
                name='check_cantidad_cuotas_positiva'
            ),
            models.CheckConstraint(
                condition=models.Q(monto_financiado__gt=0),
                name='check_monto_financiado_positivo'
            ),
        ]

    def clean(self):
        if self.forma_pago_id and self.forma_pago.tipo_pago != 'financiamiento_interno':
            raise ValidationError({
                'forma_pago': 'La forma de pago referenciada debe ser de tipo "financiamiento_interno".'
            })

        if self.operacion_id and self.forma_pago_id and self.forma_pago.operacion_id != self.operacion_id:
            raise ValidationError({
                'forma_pago': 'La forma de pago no corresponde a la operación seleccionada.'
            })

        if self.cantidad_cuotas is not None and self.cantidad_cuotas <= 0:
            raise ValidationError({'cantidad_cuotas': 'La cantidad de cuotas debe ser mayor a cero.'})

    def _obtener_tasa_default(self):
        try:
            from parametro_sistema.models import ParametroSistema
            parametro = ParametroSistema.objects.get(nombre_parametro='tasa_interes_credito_interno')
            return Decimal(parametro.valor)
        except Exception:
            return Decimal('5.00')  # valor de respaldo si no está cargado el parámetro

    def _calcular_fecha_cuota(self, numero_cuota):
        # suma "numero_cuota" meses a fecha_primera_cuota, sin dependencias externas
        mes_total = self.fecha_primera_cuota.month - 1 + (numero_cuota - 1)
        anio = self.fecha_primera_cuota.year + mes_total // 12
        mes = mes_total % 12 + 1
        import calendar
        dia = min(self.fecha_primera_cuota.day, calendar.monthrange(anio, mes)[1])
        return datetime.date(anio, mes, dia)

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        es_nuevo = self.pk is None

        if not self.fecha_primera_cuota:
            self.fecha_primera_cuota = datetime.date.today()

        if es_nuevo and self.tasa_interes_mensual is None:
            self.tasa_interes_mensual = self._obtener_tasa_default()

        if self.monto_financiado and self.cantidad_cuotas and self.tasa_interes_mensual is not None:
            interes_total = self.tasa_interes_mensual / Decimal('100') * self.cantidad_cuotas
            self.monto_cuota = (self.monto_financiado * (1 + interes_total)) / self.cantidad_cuotas
            self.monto_cuota = self.monto_cuota.quantize(Decimal('0.01'))
            self.monto_total = self.monto_cuota * self.cantidad_cuotas

        if not skip_validation:
            self.full_clean(exclude=['monto_cuota', 'monto_total'])

        super().save(*args, **kwargs)

        if es_nuevo:
            cuotas = [
                CuotaCredito(
                    credito_interno=self,
                    numero_cuota=i,
                    monto_cuota=self.monto_cuota,
                    fecha_vencimiento=self._calcular_fecha_cuota(i),
                )
                for i in range(1, self.cantidad_cuotas + 1)
            ]
            CuotaCredito.objects.bulk_create(cuotas)

    def __str__(self):
        return f"Crédito Interno Op {self.operacion_id} - {self.cantidad_cuotas} cuotas de ${self.monto_cuota}"


# =============================== CUOTA CREDITO ====================================

class CuotaCredito(models.Model):
    FORMA_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
        ('pagare', 'Pagaré'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]

    credito_interno = models.ForeignKey(
        CreditoInterno, on_delete=models.PROTECT, related_name='cuotas'
    )
    numero_cuota = models.PositiveIntegerField()
    monto_cuota = models.DecimalField(max_digits=14, decimal_places=2)
    fecha_vencimiento = models.DateField()

    monto_pagado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    fecha_pago_real = models.DateField(null=True, blank=True)
    forma_pago_cuota = models.CharField(max_length=15, choices=FORMA_PAGO_CHOICES, null=True, blank=True)
    monto_mora = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True)

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['credito_interno', 'numero_cuota'],
                name='unique_numero_cuota_por_credito'
            ),
            models.CheckConstraint(
                condition=models.Q(monto_cuota__gt=0),
                name='check_monto_cuota_positivo'
            ),
        ]

    def clean(self):
        if self.estado == 'pagada':
            if not self.fecha_pago_real:
                raise ValidationError({'fecha_pago_real': 'Obligatoria cuando la cuota está pagada.'})
            if not self.monto_pagado:
                raise ValidationError({'monto_pagado': 'Obligatorio cuando la cuota está pagada.'})
            if not self.forma_pago_cuota:
                raise ValidationError({'forma_pago_cuota': 'Obligatoria cuando la cuota está pagada.'})

    # Si se cargaron los datos de pago pero no se marcó el estado, bloquear:
    # evita que quede un pago registrado sin confirmar explicitamente el cierre de la cuota.
        if self.estado != 'pagada' and self.monto_pagado and self.fecha_pago_real and self.forma_pago_cuota:
            raise ValidationError({
                'estado': 'Cargó los datos de pago pero el estado sigue en "%s". Debe marcar el estado como "Pagada" para confirmar el registro del pago.' % self.estado
            })

        hoy = datetime.date.today()
        if self.fecha_pago_real and self.fecha_pago_real > hoy:
            raise ValidationError({'fecha_pago_real': 'La fecha de pago no puede ser futura.'})

    def save(self, *args, **kwargs):
        skip_validation = kwargs.pop('skip_validation', False)
        if not skip_validation:
            self.full_clean()
        super().save(*args, **kwargs)

    # Si todas las cuotas del crédito están pagadas, marca el crédito como completado
        if self.estado == 'pagada':
            pendientes = self.credito_interno.cuotas.exclude(estado='pagada').exists()
            if not pendientes:
                self.credito_interno.estado = 'completado'
                self.credito_interno.save(skip_validation=True)

    def __str__(self):
        return f"Cuota {self.numero_cuota}/{self.credito_interno.cantidad_cuotas} - {self.credito_interno}"