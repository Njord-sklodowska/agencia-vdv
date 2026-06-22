from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Cliente(models.Model):

    TIPO_PERSONA_CHOICES = [
        ('fisica', 'Fisica'),
        ('juridica', 'Juridica'),
    ]

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    tipo_persona = models.CharField(
        max_length=10,
        choices=TIPO_PERSONA_CHOICES
    )

    dni_cuit = models.CharField(
        max_length=20,
        unique=True
    )

    cuil = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    condicion_iva = models.CharField(
        max_length=100
    )

    nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    apellido = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    razon_social = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    nombre_fantasia = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True
    )

    nacionalidad = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=20
    )

    telefono_alternativo = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    email = models.EmailField(
        null=True,
        blank=True
    )

    domicilio_real = models.CharField(
        max_length=255
    )

    domicilio_fiscal = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    observaciones = models.TextField(
        blank=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activo'
    )

    fecha_alta = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        if self.tipo_persona == 'fisica':

            if not self.nombre or not self.nombre.strip():
                raise ValidationError({
                    'nombre': 'El nombre es obligatorio.'
                })

            if not self.apellido or not self.apellido.strip():
                raise ValidationError({
                    'apellido': 'El apellido es obligatorio.'
                })

            if not self.cuil:
                raise ValidationError({
                    'cuil': 'El CUIL es obligatorio.'
                })

        if self.tipo_persona == 'juridica':

            if not self.razon_social or not self.razon_social.strip():
                raise ValidationError({
                    'razon_social': 'La razón social es obligatoria.'
                })

        if self.fecha_nacimiento:

            if self.fecha_nacimiento >= timezone.now().date():
                raise ValidationError({
                    'fecha_nacimiento': 'La fecha debe ser anterior a hoy.'
                })

            hoy = timezone.now().date()

            edad = (
                hoy.year
                - self.fecha_nacimiento.year
                - (
                    (hoy.month, hoy.day)
                    < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
                )
            )

            if edad < 18:
                raise ValidationError({
                    'fecha_nacimiento': 'El cliente debe ser mayor de 18 años.'
                })

        if not self.domicilio_fiscal:
            self.domicilio_fiscal = self.domicilio_real

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):

        if self.tipo_persona == 'fisica':
            return f"{self.apellido}, {self.nombre}"

        return self.razon_social