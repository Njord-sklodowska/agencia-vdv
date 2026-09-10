from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from inventario.models import Vehiculo


class TipoDocumento(models.Model):
    """
    Catálogo de tipos de documento (formulario_08, título, cédula, informe de
    dominio, informe de multas, patentes, verificación, F12, VTV, prenda,
    manual, duplicado de llave, otro — según RF08).

    Se modela como tabla en vez de ENUM fijo para poder activar/desactivar
    tipos y marcar cuáles son obligatorios o tienen vencimiento, sin tocar
    código ni migraciones.
    """

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    es_obligatorio = models.BooleanField(
        default=True,
        help_text="Si es obligatorio, se exige para considerar la documentación del vehículo 'Completa' (RN-18).",
    )
    requiere_vencimiento = models.BooleanField(
        default=False,
        help_text="Marcar para documentos con validez temporal (ej. VTV, Informe de Multas).",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Gestor(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="activo")
    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gestor"
        verbose_name_plural = "Gestores"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class DocumentacionVehiculo(models.Model):
    # ENUM alineado al modelo de datos del documento del proyecto
    # (sección 16 - Documentacion_Vehiculo)
    ESTADO_DOC_CHOICES = [
        ("pendiente", "Pendiente"),
        ("recibido", "Recibido"),
        ("en_tramite", "En Trámite"),
        ("completado", "Completado"),
    ]

    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name="documentos"
    )
    tipo_documento = models.ForeignKey(
        TipoDocumento, on_delete=models.PROTECT, related_name="documentos_vehiculo"
    )
    estado_documento = models.CharField(
        max_length=20, choices=ESTADO_DOC_CHOICES, default="pendiente"
    )

    gestor = models.ForeignKey(
        Gestor, on_delete=models.SET_NULL, null=True, blank=True, related_name="tramites"
    )

    fecha_recepcion = models.DateField(
        null=True, blank=True, help_text="Fecha de recepción del documento."
    )
    fecha_entrega_gestor = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de entrega física al gestor externo (RN-19). Se completa cuando estado_documento pasa a en_tramite.",
    )
    fecha_estimada_devolucion = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha estimada de devolución definida por el administrativo al entregar al gestor (RN-19).",
    )
    fecha_devolucion_real = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en que el gestor devolvió efectivamente el documento. Se completa cuando estado_documento pasa a completado.",
    )
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
        help_text="Aplica a documentos con validez temporal (VTV, Informe de Multas). Null para documentos sin vencimiento (título, cédula, formulario 08).",
    )

    archivo_pdf = models.FileField(
        upload_to="documentos_pdf/%Y/%m/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    observaciones = models.TextField(blank=True, null=True)

    activo = models.BooleanField(default=True)
    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documentación de Vehículo"
        verbose_name_plural = "Documentaciones de Vehículos"
        ordering = ["-fecha_alta"]

    def __str__(self):
        identificador = self.vehiculo.patente or self.vehiculo.vin
        return f"{identificador} - {self.tipo_documento.nombre} ({self.get_estado_documento_display()})"

    @property
    def esta_vencido(self):
        if self.fecha_vencimiento:
            return self.fecha_vencimiento < timezone.now().date()
        return False

    @staticmethod
    def documentos_faltantes(vehiculo):
        """
        RN-18: por cada tipo de documento obligatorio, informa si al
        vehículo le falta ese documento y por qué motivo puntual:

          - 'no_iniciado': nunca se creó un registro para ese tipo.
          - 'vencido': existe, pero su fecha_vencimiento ya pasó.
          - <estado_documento> (ej. 'pendiente', 'en_tramite'): existe,
            pero todavía no está 'completado'.

        Si un tipo obligatorio ya está 'completado' y no vencido, no
        aparece en el resultado.

        Devuelve una lista de diccionarios (no un queryset) para que sea
        directamente serializable en una respuesta JSON de la API.
        """
        tipos_obligatorios = TipoDocumento.objects.filter(es_obligatorio=True, activo=True)
        hoy = timezone.now().date()
        faltantes = []

        for tipo in tipos_obligatorios:
            # Si hubiera más de un registro activo para el mismo tipo
            # (ej. se corrigió un documento rechazado con uno nuevo),
            # se evalúa el más reciente.
            documento = (
                DocumentacionVehiculo.objects.filter(
                    vehiculo=vehiculo, tipo_documento=tipo, activo=True
                )
                .order_by("-fecha_alta")
                .first()
            )

            if documento is None:
                faltantes.append(
                    {
                        "tipo_documento_id": tipo.id,
                        "tipo_documento": tipo.nombre,
                        "motivo": "no_iniciado",
                        "detalle": "No existe ningún registro de este documento para el vehículo.",
                    }
                )
                continue

            if documento.fecha_vencimiento and documento.fecha_vencimiento < hoy:
                faltantes.append(
                    {
                        "tipo_documento_id": tipo.id,
                        "tipo_documento": tipo.nombre,
                        "documento_id": documento.id,
                        "motivo": "vencido",
                        "detalle": f"El documento está vencido desde el {documento.fecha_vencimiento}.",
                    }
                )
                continue

            if documento.estado_documento != "completado":
                faltantes.append(
                    {
                        "tipo_documento_id": tipo.id,
                        "tipo_documento": tipo.nombre,
                        "documento_id": documento.id,
                        "motivo": documento.estado_documento,
                        "detalle": f"El documento está en estado '{documento.get_estado_documento_display()}'.",
                    }
                )

        return faltantes

    @staticmethod
    def documentacion_completa(vehiculo):
        """
        RN-18: un vehículo vendido no puede entregarse hasta que su
        documentación sea 'Completa'. Reutiliza documentos_faltantes()
        para no duplicar la regla en dos lugares: si la lista de
        faltantes está vacía, la documentación está completa.

        Pensado para ser consumido desde la app 'ventas' antes de permitir
        marcar una operación como entregada.
        """
        return len(DocumentacionVehiculo.documentos_faltantes(vehiculo)) == 0
 