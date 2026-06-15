from django.contrib import admin
from .models import ParametroSistema


@admin.register(ParametroSistema)
class ParametroSistemaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_parametro',
        'valor',
        'tipo_dato',
        'fecha_alta',
        'updated_at'
    )

    search_fields = (
        'nombre_parametro',
        'descripcion'
    )

    list_filter = (
        'tipo_dato',
    )