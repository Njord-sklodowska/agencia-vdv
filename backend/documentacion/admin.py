from django.contrib import admin

from .models import DocumentacionVehiculo, Gestor, TipoDocumento


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "es_obligatorio", "requiere_vencimiento", "activo")
    list_filter = ("es_obligatorio", "requiere_vencimiento", "activo")
    search_fields = ("nombre",)


@admin.register(Gestor)
class GestorAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "telefono", "email", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre", "apellido", "email")


@admin.register(DocumentacionVehiculo)
class DocumentacionVehiculoAdmin(admin.ModelAdmin):
    list_display = (
        "vehiculo",
        "tipo_documento",
        "estado_documento",
        "gestor",
        "fecha_vencimiento",
        "esta_vencido",
        "activo",
    )
    list_filter = ("estado_documento", "activo", "tipo_documento")
    search_fields = ("vehiculo__patente", "vehiculo__vin")
    autocomplete_fields = ("vehiculo", "tipo_documento", "gestor")
