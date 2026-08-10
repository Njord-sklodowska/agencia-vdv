from django.db import models
from django.core.exceptions import ValidationError

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)

    ESTADOS = [
        ('activa', 'Activa'),
        ('inactiva', 'Inactiva'),
    ]

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='activa'
    )

    def clean(self):
        """Validaciones del modelo"""
        if self.telefono:
            limpio = self.telefono.replace('-', '').replace('.', '').replace(' ', '')
            if not limpio.isdigit():
                raise ValidationError({'telefono': 'El teléfono solo debe contener números.'})
            if len(limpio) not in [10, 11]:
                raise ValidationError({'telefono': f'El teléfono debe tener 10 u 11 dígitos. Tiene {len(limpio)}.'})
            self.telefono = limpio

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre