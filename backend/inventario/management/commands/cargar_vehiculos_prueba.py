
from django.core.management.base import BaseCommand
from inventario.models import Vehiculo, Marca, Modelo, VehiculoUsado
from sucursal.models import Sucursal
from django.contrib.auth import get_user_model
import datetime
import random

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Carga vehículos de prueba (0km y usados) para testing'

    def handle(self, *args, **options):
        sucursal = Sucursal.objects.first()
        if not sucursal:
            self.stdout.write(self.style.ERROR('No hay sucursales. Creá una primero.'))
            return

        usuario = Usuario.objects.first()
        if not usuario:
            self.stdout.write(self.style.ERROR('No hay usuarios. Creá uno primero (createsuperuser).'))
            return

        marca_toyota, _ = Marca.objects.get_or_create(nombre='Toyota')
        marca_ford, _ = Marca.objects.get_or_create(nombre='Ford')
        marca_vw, _ = Marca.objects.get_or_create(nombre='Volkswagen')

        modelo_corolla, _ = Modelo.objects.get_or_create(
            nombre='Corolla', marca=marca_toyota, carroceria='sedan'
        )
        modelo_ranger, _ = Modelo.objects.get_or_create(
            nombre='Ranger', marca=marca_ford, carroceria='pickup'
        )
        modelo_gol, _ = Modelo.objects.get_or_create(
            nombre='Gol', marca=marca_vw, carroceria='hatchback'
        )

        modelos = [modelo_corolla, modelo_ranger, modelo_gol]

        # ---- 0KM ----
        vehiculos_0km = []
        for i in range(5):
            vin = f"0KM{i:014d}"  # 17 caracteres
            v = Vehiculo(
                sucursal=sucursal,
                marca=random.choice(modelos).marca,
                modelo=random.choice(modelos),
                condicion_vehiculo='0km',
                vin=vin,
                anio=2026,
                color=random.choice(['blanco', 'negro', 'gris', 'rojo']),
                precio_costo=random.randint(15000000, 25000000),
                precio=random.randint(18000000, 30000000),
                descripcion_tecnica='Vehículo de prueba 0km',
                combustible=random.choice(['nafta', 'diesel']),
                transmision=random.choice(['manual', 'automatica']),
                puertas=4,
                motor='1.6',
                numero_serie_motor=f'MOTOR-0KM-{i}',
                kilometraje=0,
            )
            v.save()
            vehiculos_0km.append(v)
            self.stdout.write(self.style.SUCCESS(f'0km creado: {v}'))

        # ---- USADOS ----
        for i in range(5):
            vin = f"USD{i:014d}"
            patente = f"AB{100+i}CD"
            v = Vehiculo(
                sucursal=sucursal,
                marca=random.choice(modelos).marca,
                modelo=random.choice(modelos),
                condicion_vehiculo='usado',
                vin=vin,
                patente=patente,
                anio=random.randint(2015, 2022),
                color=random.choice(['blanco', 'negro', 'gris', 'azul']),
                precio_costo=random.randint(5000000, 12000000),
                precio=random.randint(6000000, 15000000),
                descripcion_tecnica='Vehículo de prueba usado',
                combustible=random.choice(['nafta', 'diesel', 'gnc']),
                transmision=random.choice(['manual', 'automatica']),
                puertas=random.choice([2, 4, 5]),
                motor='1.6',
                numero_serie_motor=f'MOTOR-USD-{i}',
                kilometraje=random.randint(20000, 90000),
                procedencia=random.choice(['compra_directa', 'parte_de_pago']),
            )
            v.save()
            self.stdout.write(self.style.SUCCESS(f'Usado creado: {v}'))

            # Crear evaluación para algunos (no todos, para tener casos sin evaluación también)
            if i % 2 == 0:
                VehiculoUsado.objects.create(
                    vehiculo=v,
                    usuario_autoriza=usuario,
                    precio_tasacion_final=v.precio_costo,
                    fecha_ingreso=datetime.date.today(),
                    estado_cubierta='bueno',
                    estado_motor='bueno',
                    estado_chapa_pintura='regular',
                    estado_interior='bueno',
                )
                self.stdout.write(self.style.SUCCESS(f'  → con evaluación registrada'))
            else:
                self.stdout.write(self.style.WARNING(f'  → SIN evaluación (para probar validación)'))

        self.stdout.write(self.style.SUCCESS('\n¡Listo! Se crearon 5 vehículos 0km y 5 usados.'))