from django.contrib import admin
from .models import Usuario, Rol
from sucursal.models import Sucursal

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Sucursal)