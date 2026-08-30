
from django.contrib import admin, messages
from django.utils.html import mark_safe
from .models import Vehiculo, Marca, Modelo, Fotografia_Vehiculo, Taller, VehiculoUsado, TrasladoVehiculo

# --- Inlines ---
class FotografiaInline(admin.TabularInline):
    model = Fotografia_Vehiculo
    extra = 0  # elimino las filas extras
    max_num = 10
    fields = ('orden', 'es_portada', 'archivo', 'imagen_tag')
    readonly_fields = ('imagen_tag', 'tamano_bytes', 'mime_type')
    ordering = ('orden',) # Esto garantiza que siempre se vean ordenadas

    def imagen_tag(self, obj):
        if obj.archivo:
            return mark_safe(f'<a href="{obj.archivo.url}" target="_blank">'
                             f'<img src="{obj.archivo.url}" width="100" /></a>')
        return "No hay imagen"
    imagen_tag.short_description = 'Previsualización'

# --- ModelAdmins ---
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('marca', 'nombre', 'carroceria')
    list_filter = ('marca', 'carroceria')
    search_fields = ('nombre', 'marca__nombre')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información General', {
            'fields': ('sucursal', 'marca', 'modelo', 'condicion_vehiculo', 'estado', 'entregado', 'activo')
        }),
        ('Documentación e Identificación', {
            'fields': ('vin', 'patente', 'numero_serie_motor', 'procedencia')
        }),
        ('Detalles Técnicos', {
            'fields': ('anio', 'color', 'kilometraje', 'combustible', 'transmision', 'puertas', 'motor', 'traccion')
        }),
        ('Precios', {
            'fields': ('precio_costo', 'precio')
        }),
        ('Descripción', {
            'fields': ('descripcion_tecnica',)
        }),
    )
    
    inlines = [FotografiaInline]
    list_display = ('marca', 'modelo', 'patente', 'estado', 'entregado', 'precio', 'activo')
    list_filter = ('estado', 'entregado', 'activo' , 'condicion_vehiculo', 'marca')
    search_fields = ('patente', 'vin')

    # 1. deshabilita el borrado físico total (reemplazado por desactivación)
    def has_delete_permission(self, request, obj=None):
        return False

    # 2. Acciones personalizadas (Reemplaza el borrado masivo por desactivación)
    actions = ['desactivar_vehiculos']

    def desactivar_vehiculos(self, request, queryset):
        # Filtramos los que SÍ se pueden desactivar
        a_desactivar = queryset.exclude(estado__in=['vendido', 'reservado'])
        bloqueados = queryset.filter(estado__in=['vendido', 'reservado'])
        
        if bloqueados.exists():
            self.message_user(
                request, 
                f"No se pudieron desactivar {bloqueados.count()} vehículos (estado vendido/reservado).", 
                level=messages.ERROR
            )
        
        # Ejecutamos el borrado lógico (soft_delete)
        for obj in a_desactivar:
            obj.soft_delete()
            
        if a_desactivar.exists():
            self.message_user(request, f"Se desactivaron correctamente {a_desactivar.count()} vehículos.")
    
    desactivar_vehiculos.short_description = "Desactivar vehículos seleccionados (Soft Delete)"

    # Sobrescribimos delete_queryset para evitar cualquier ejecución física accidental
    def delete_queryset(self, request, queryset):
        self.message_user(request, "El borrado físico está deshabilitado. Use la acción de 'Desactivar'.", level=messages.ERROR)

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
    


@admin.register(Fotografia_Vehiculo)
class FotografiaVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'imagen_tag', 'es_portada', 'orden')
    readonly_fields = ('imagen_tag', 'tamano_bytes', 'mime_type')
    
    def imagen_tag(self, obj):
        if obj.archivo:
            return mark_safe(f'<a href="{obj.archivo.url}" target="_blank">'
                             f'<img src="{obj.archivo.url}" width="150" /></a>')
        return "Sin imagen"
    imagen_tag.short_description = 'Imagen'

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)

@admin.register(VehiculoUsado)
class VehiculoUsadoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'taller', 'precio_tasacion_final', 'fecha_ingreso')
    list_filter = ('taller',)
    search_fields = ('vehiculo__patente',)
    readonly_fields = ('fecha_alta', 'updated_at')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'vehiculo':
            kwargs['queryset'] = Vehiculo.objects.filter(condicion_vehiculo='usado')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
        

@admin.register(TrasladoVehiculo)
class TrasladoVehiculoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'sucursal_origen', 'sucursal_destino', 'estado', 'fecha_traslado')
    list_filter = ('estado',)
    search_fields = ('vehiculo__patente',)
    readonly_fields = ('fecha_alta', 'updated_at')


