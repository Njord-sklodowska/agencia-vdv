from django.contrib.auth.models import AbstractUser
from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


ESTADOS = (
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
)


class Usuario(AbstractUser):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)
    sucursal = models.ForeignKey(
        'sucursal.Sucursal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
)

    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')

    fecha_alta = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username