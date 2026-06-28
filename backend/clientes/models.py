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
    
    CONDICION_IVA_CHOICES = [
        ('responsable_inscripto', 'Responsable Inscripto'),
        ('monotributista', 'Monotributista'),
        ('exento', 'Exento'),
        ('consumidor_final', 'Consumidor Final'),
    ]

    CUIL_PREFIJOS_VALIDOS = ['20', '23', '24', '27']
    CUIT_PREFIJOS_JURIDICA = ['30', '33', '34']

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
    	choices=CONDICION_IVA_CHOICES,
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

    def _limpiar_numeros(self, value):
        if not value:
            return ''
        return value.replace('-', '').replace('.', '').replace(' ', '')

    def _validar_dni_cuit(self):
        """Valida DNI (física) o CUIT (jurídica) y guarda limpio (sin guiones)"""
        if not self.dni_cuit:
            return
        
        limpio = self._limpiar_numeros(self.dni_cuit)
        
        if not limpio.isdigit():
            raise ValidationError({'dni_cuit': 'El DNI/CUIT solo debe contener números.'})
        
        if self.tipo_persona == 'fisica':
            # DNI: exactamente 8 dígitos
            if len(limpio) != 8:
                raise ValidationError({'dni_cuit': f'El DNI debe tener exactamente 8 dígitos. Tiene {len(limpio)}.'})
            # Guardar limpio, sin guiones
            self.dni_cuit = limpio
            
        elif self.tipo_persona == 'juridica':
            # CUIT: exactamente 11 dígitos
            if len(limpio) != 11:
                raise ValidationError({'dni_cuit': f'El CUIT debe tener exactamente 11 dígitos. Tiene {len(limpio)}.'})
            
            # Validar prefijo válido para jurídica
            prefijo = limpio[:2]
            if prefijo not in self.CUIT_PREFIJOS_JURIDICA:
                raise ValidationError({'dni_cuit': f'El CUIT debe empezar con 30, 33 o 34. Empieza con {prefijo}.'})
            
            # Guardar limpio, sin guiones
            self.dni_cuit = limpio

    def _validar_cuil(self):
        """Valida CUIL para persona física y guarda limpio (sin guiones)"""
        # El CUIL solo aplica para persona física
        if self.tipo_persona != 'fisica':
            self.cuil = None
            return
        
        # Para persona física, el CUIL es obligatorio
        if not self.cuil:
            return  # Será validado como campo requerido en clean()
        
        limpio = self._limpiar_numeros(self.cuil)
        
        if not limpio.isdigit():
            raise ValidationError({'cuil': 'El CUIL solo debe contener números.'})
        
        if len(limpio) != 11:
            raise ValidationError({'cuil': f'El CUIL debe tener exactamente 11 dígitos. Tiene {len(limpio)}.'})
        
        # Validar prefijo válido
        prefijo = limpio[:2]
        if prefijo not in self.CUIL_PREFIJOS_VALIDOS:
            raise ValidationError({'cuil': f'El CUIL debe empezar con 20, 23, 24 o 27. Empieza con {prefijo}.'})
        
        # Los 8 dígitos centrales deben coincidir con el DNI
        dni_central = limpio[2:10]
        if self.dni_cuit and dni_central != self.dni_cuit:
            raise ValidationError({'cuil': f'Los 8 dígitos centrales del CUIL ({dni_central}) deben coincidir con el DNI ({self.dni_cuit}).'})
        
        # Guardar limpio, sin guiones
        self.cuil = limpio

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

        self._validar_dni_cuit()
        self._validar_cuil()

        if not self.telefono.isdigit():
            raise ValidationError({
                'telefono': 'El teléfono debe contener solo números.'
            })

        if len(self.telefono) not in [10, 11]:
            raise ValidationError({
                'telefono': 'El teléfono debe tener 10 u 11 dígitos.'
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
