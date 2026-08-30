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

    first_name = None
    last_name = None

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT
    )

    sucursal = models.ForeignKey(
        'sucursal.Sucursal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=80)

    apellido = models.CharField(max_length=80)

    email = models.EmailField(
        max_length=150,
        unique=True
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='activo'
    )

    intentos_fallidos = models.PositiveIntegerField(
        default=0
    )

    fecha_bloqueo = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_alta = models.DateField(
        auto_now_add=True
    )

    fecha_baja = models.DateField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if self.fecha_baja:
            self.estado = 'inactivo'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username