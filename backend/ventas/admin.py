
from django.contrib import admin
from .models import OperacionVenta, FormaPago, Anticipo
from django.contrib import messages


class FormaPagoInline(admin.TabularInline):
    model = FormaPago
    extra = 0
    fields = ('tipo_pago', 'monto', 'cotizacion_dolar', 'fecha_registro')
    readonly_fields = ('fecha_registro',)


@admin.register(OperacionVenta)
class OperacionVentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo_vendido', 'cliente', 'estado', 'precio_final', 'fecha_operacion')
    list_filter = ('estado', 'sucursal')
    search_fields = ('vehiculo_vendido__patente', 'vehiculo_vendido__vin')
    readonly_fields = readonly_fields = ('fecha_alta', 'updated_at', 'fecha_cambio_estado', 'precio_final', 'precio_original')
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
            obj.valor_vehiculo_usado = obj.vehiculo_usado_entregado.precio_costo

        obj.precio_final = (obj.precio_original or 0) - (obj.descuento_aplicado or 0) - (obj.valor_vehiculo_usado or 0)
        obj.full_clean(exclude=['precio_final'])
        super().save_model(request, obj, form, change)

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