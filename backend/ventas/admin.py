
from django.contrib import admin, messages
from .models import OperacionVenta, FormaPago, Anticipo, TituloCredito, RegistroCobro, EntidadFinanciera, CreditoInterno, CuotaCredito, FinanciamientoExterno
from django.core.exceptions import ValidationError

class FormaPagoInline(admin.TabularInline):
    model = FormaPago
    extra = 0
    fields = ('tipo_pago', 'monto', 'cotizacion_dolar', 'fecha_registro', 'titulo_estado')
    readonly_fields = ('fecha_registro', 'titulo_estado')

    def titulo_estado(self, obj):
        if obj.tipo_pago not in ['cheque', 'pagare']:
            return '—'
        if hasattr(obj, 'titulo_credito'):
            return 'Título registrado'
        return 'Falta título de crédito'
    titulo_estado.short_description = 'Título de Crédito'

@admin.register(OperacionVenta)
class OperacionVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_boleto', 'vehiculo_vendido', 'cliente', 'estado', 'precio_final', 'fecha_operacion')
    list_filter = ('estado', 'sucursal')
    search_fields = ('vehiculo_vendido__patente', 'vehiculo_vendido__vin')
    readonly_fields = ('fecha_alta', 'updated_at', 'fecha_cambio_estado', 'precio_final', 'precio_original')
    inlines = [FormaPagoInline]

    fieldsets = (
        ('Información General', {
            'fields': ('sucursal', 'cliente', 'cliente_cotitular', 'vendedor', 'usuario_registro', 'anticipo')
        }),
        ('Vehículos', {
            'fields': ('vehiculo_vendido', 'vehiculo_usado_entregado')
        }),
        ('Datos Comerciales', {
            'fields': ('fecha_operacion', 'precio_original', 'descuento_aplicado', 'precio_final')
        }),
        ('Gestión', {
            'fields': ('estado', 'numero_boleto', 'ruta_boleto_pdf', 'observaciones')
        }),
        ('Fechas', {
            'fields': ('fecha_alta', 'updated_at', 'fecha_cambio_estado')
        }),
    )

    def save_model(self, request, obj, form, change):
        if change:
            original = OperacionVenta.objects.get(pk=obj.pk)
            if original.estado == 'borrador' and obj.estado == 'confirmada':
                self.message_user(
                    request,
                    'No se puede confirmar una operación desde el admin. Use el endpoint /confirmar/ de la API.',
                    level=messages.ERROR
                )
                obj.estado = 'borrador'
        
        if obj.vehiculo_vendido:
            obj.precio_original = obj.vehiculo_vendido.precio
        if obj.vehiculo_usado_entregado:
            obj.valor_vehiculo_usado = obj.vehiculo_usado_entregado.precio_costo or 0 

        obj.precio_final = (obj.precio_original or 0) - (obj.descuento_aplicado or 0) - (obj.valor_vehiculo_usado or 0)
        
        try:
            obj.full_clean(exclude=['precio_final', 'precio_original', 'valor_vehiculo_usado'])
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                for field, errors in e.message_dict.items():
                    for error in errors:
                        self.message_user(request, f"{field}: {error}", level=messages.ERROR)
            else:
                self.message_user(request, str(e), level=messages.ERROR)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_related(self, request, form, formsets, change):
        """
        Este método se ejecuta en el Admin justo después de guardar la operación 
        y sus inlines (Formas de Pago). Aquí replicamos la lógica de la API.
        """
        super().save_related(request, form, formsets, change)
        
        operacion = form.instance
        
        # Revisamos si alguna de las formas de pago de esta operación es de tipo financiamiento interno
        for forma_pago in operacion.formas_pago.all(): # (Asegúrate de tener el related_name correcto, ej: formas_pago)
            if getattr(forma_pago, 'tipo_pago', None) == 'financiamiento_interno':
                # Verificamos si ya tiene un crédito interno asociado para no duplicarlo
                from .models import CreditoInterno
                if not hasattr(forma_pago, 'credito_interno') and not CreditoInterno.objects.filter(operacion=operacion).exists():
                    pass

@admin.register(Anticipo)
class AnticipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'cliente', 'monto', 'forma_pago', 'estado', 'fecha_anticipo')
    list_filter = ('estado', 'forma_pago')
    search_fields = ('vehiculo__patente', 'vehiculo__vin')
    readonly_fields = ('fecha_alta', 'updated_at')

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FormaPago)
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ('operacion', 'tipo_pago', 'monto', 'fecha_registro')
    list_filter = ('tipo_pago',)
    readonly_fields = ('fecha_registro',)

@admin.register(TituloCredito)
class TituloCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'numero_documento', 'monto', 'vehiculo_modelo', 'estado', 'fecha_recepcion', 'fecha_cobro')
    list_filter = ('tipo', 'estado', 'banco_emisor')
    search_fields = ('numero_documento', 'titular', 'banco_emisor')
    readonly_fields = (
        'fecha_alta', 'updated_at',
        'fecha_acreditacion', 'forma_acreditacion', 
    )

    fieldsets = (
        ('Referencia (elegir solo una)', {
            'fields': ('forma_pago', 'anticipo')
        }),
        ('Datos del Documento', {
            'fields': ('tipo', 'numero_documento', 'banco_emisor', 'titular')
        }),
        ('Plazos', {
            'fields': ('plazo_dias', 'fecha_vencimiento_manual', 'fecha_recepcion', 'fecha_cobro')
        }),
        ('Acreditación (se completa automáticamente al registrar el cobro)', {
            'fields': ('fecha_acreditacion', 'forma_acreditacion')
        }),
        ('Estado y Montos', {
            'fields': ('monto', 'interes_mora', 'estado', 'observaciones')
        }),
        ('Fechas de Sistema', {
            'fields': ('fecha_alta', 'updated_at')
        }),
    )

    def vehiculo_modelo(self, obj):
        operacion = None
        if obj.forma_pago and obj.forma_pago.operacion:
            operacion = obj.forma_pago.operacion
        elif obj.anticipo and obj.anticipo.operacion_aplicado:
            operacion = obj.anticipo.operacion_aplicado
        elif obj.anticipo and obj.anticipo.vehiculo:
            return str(obj.anticipo.vehiculo)

        if operacion and operacion.vehiculo_vendido:
            return str(operacion.vehiculo_vendido)
        
        return '—'
    
    vehiculo_modelo.short_description = 'Vehículo'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
   
@admin.register(RegistroCobro)
class RegistroCobroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_pago_real', 'monto_pagado', 'forma_cobro', 'forma_acreditacion_cheque', 'pago_con_mora')
    list_filter = ('forma_cobro', 'pago_con_mora')
    search_fields = ('titulo__numero_documento',)
    readonly_fields = ('fecha_alta',)

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        titulo_id = request.GET.get('titulo')
        if titulo_id:
            from .models import TituloCredito
            titulo = TituloCredito.objects.filter(pk=titulo_id).first()
            if titulo and titulo.tipo == 'cheque':
                initial['forma_cobro'] = 'cheque'
        return initial

@admin.register(EntidadFinanciera)
class EntidadFinancieraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado', 'fecha_alta')
    list_filter = ('estado',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(FinanciamientoExterno)
class FinanciamientoExternoAdmin(admin.ModelAdmin):
    list_display = ('id', 'operacion', 'entidad', 'monto_aprobado', 'numero_credito', 'fecha_aprobacion')
    list_filter = ('entidad',)
    search_fields = ('numero_credito', 'operacion__id')
    ordering = ('-fecha_alta',)


class CuotaCreditoInline(admin.TabularInline):
    model = CuotaCredito
    extra = 0
    readonly_fields = ('numero_cuota', 'monto_cuota', 'fecha_vencimiento')
    fields = ('numero_cuota', 'monto_cuota', 'fecha_vencimiento', 'estado', 'monto_pagado', 'fecha_pago_real')


@admin.register(CreditoInterno)
class CreditoInternoAdmin(admin.ModelAdmin):
    list_display = ('id', 'operacion', 'monto_financiado', 'cantidad_cuotas', 'monto_cuota', 'estado')
    list_filter = ('estado',)
    inlines = [CuotaCreditoInline]
    readonly_fields = ('monto_cuota', 'monto_total')


@admin.register(CuotaCredito)
class CuotaCreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'credito_interno', 'numero_cuota', 'fecha_vencimiento', 'estado', 'monto_pagado')
    list_filter = ('estado',)
    search_fields = ('credito_interno__id',)

