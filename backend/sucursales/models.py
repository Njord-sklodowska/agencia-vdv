from django.db import models

class SucursalTemp(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)