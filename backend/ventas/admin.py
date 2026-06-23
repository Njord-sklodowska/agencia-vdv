
from django.contrib import admin, messages
from .models import OperacionVenta, FormaPago, Anticipo, TituloCredito, RegistroCobro
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
            return '✅ Título registrado'
        return '⚠️ Falta título de crédito'
    titulo_estado.short_description = 'Título de Crédito'


@admin.register(OperacionVenta)
class OperacionVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo_vendido', 'cliente', 'estado', 'precio_final', 'fecha_operacion')
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
            obj.valor_vehiculo_usado = obj.vehiculo_usado_entregado.precio_costo or 0  # ← or 0

        obj.precio_final = (obj.precio_original or 0) - (obj.descuento_aplicado or 0) - (obj.valor_vehiculo_usado or 0)
        
        try:
            obj.full_clean(exclude=['precio_final', 'precio_original', 'valor_vehiculo_usado'])  # ← exclude ampliado
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
    list_display = ('id', 'tipo', 'numero_documento', 'monto', 'estado', 'fecha_recepcion', 'fecha_cobro')
    list_filter = ('tipo', 'estado', 'banco_emisor')
    search_fields = ('numero_documento', 'titular', 'banco_emisor')
    readonly_fields = (
        'fecha_alta', 'updated_at',
        'fecha_acreditacion', 'forma_acreditacion', 
    )

    fieldsets = (
        ('Origen', {
            'fields': ('forma_pago', 'anticipo', 'documento_origen')
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
        

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'documento_origen':
            kwargs['queryset'] = TituloCredito.objects.filter(estado__in=['rechazado', 'en_gestion'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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