from django.db import models
from rol.models import Rol

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre