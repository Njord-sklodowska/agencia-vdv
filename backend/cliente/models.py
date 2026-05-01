from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    TIPO_CHOICES = [
        ('comprador', 'Comprador'),
        ('vendedor', 'Vendedor'),
        ('ambos', 'Comprador y Vendedor'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='comprador')

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"