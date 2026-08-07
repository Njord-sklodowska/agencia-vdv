from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'dni_cuit',
        'tipo_persona',
        'nombre',
        'apellido',
        'razon_social',
        'telefono',
        'email',
        'estado',
        'fecha_alta'
    )

    list_filter = (
        'tipo_persona',
        'estado',
        'condicion_iva'
    )

    search_fields = (
        'dni_cuit',
        'cuil',
        'nombre',
        'apellido',
        'razon_social',
        'nombre_fantasia',
        'telefono',
        'email'
    )

    readonly_fields = (
        'fecha_alta',
        'updated_at'
    )

    ordering = (
        '-fecha_alta',
    )