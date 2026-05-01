from django.db import models
from usuario.models import Usuario

class LogAuditoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    accion = models.CharField(max_length=255)
    tabla_afectada = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} - {self.fecha}"