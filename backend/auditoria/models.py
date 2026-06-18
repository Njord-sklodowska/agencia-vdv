from django.db import models
from django.conf import settings


class LogAuditoria(models.Model):

    ACCIONES = [
        ('CREAR', 'Crear'),
        ('MODIFICAR', 'Modificar'),
        ('ELIMINAR', 'Eliminar'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]

    usuario = models.ForeignKey('sucursal.Sucursal',
        on_delete=models.PROTECT,
        related_name='logs_auditoria'
    )

    accion = models.CharField(
        max_length=20,
        choices=ACCIONES
    )

    modulo = models.CharField(
        max_length=100
    )

    tabla_afectada = models.CharField(
        max_length=100
    )

    registro_id = models.IntegerField(
        null=True,
        blank=True
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.modulo}"