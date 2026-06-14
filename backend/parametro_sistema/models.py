from django.db import models

# Create your models here.
from django.db import models


class ParametroSistema(models.Model):
    nombre_parametro = models.CharField(
        max_length=100,
        unique=True
    )

    valor = models.CharField(
        max_length=255
    )

    tipo_dato = models.CharField(
        max_length=30
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    fecha_alta = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "Parametro_Sistema"
        verbose_name = "Parámetro del Sistema"
        verbose_name_plural = "Parámetros del Sistema"

    def __str__(self):
        return self.nombre_parametro