# inventario/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from inventario.models import Vehiculo, Marca, Modelo
from sucursal.models import Sucursal
from inventario.serializers import VehiculoUsadoSerializer


class VehiculoModelTest(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test', direccion='Test', ciudad='Test', provincia='Test'
        )
        self.marca = Marca.objects.create(nombre="Toyota")
        self.modelo = Modelo.objects.create(
            nombre="Corolla", marca=self.marca, carroceria="sedan"
        )
        self.datos_base = {
            'sucursal': self.sucursal,
            'marca': self.marca,
            'modelo': self.modelo,
            'color': 'blanco',
            'precio_costo': 10000,
            'precio': 12000,
            'descripcion_tecnica': 'test',
            'combustible': 'nafta',
            'transmision': 'manual',
            'puertas': 4,
            'motor': '1.6',
            'numero_serie_motor': 'MOTOR123',
        }

    def test_0km_valido(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='0km', anio=2025, vin='AAAAAAAAAAAAAAAAA')
        v.full_clean()

    def test_0km_no_puede_tener_patente(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='0km', anio=2025, patente='AA123BB', vin='BBBBBBBBBBBBBBBBB')
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_0km_kilometraje_maximo_500(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='0km', anio=2025, kilometraje=501, vin='CCCCCCCCCCCCCCCCC')
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_vin_invalido_con_letra_i(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='0km', vin='AAAAAAAAAAAAAAAAI', anio=2025)
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_usado_valido(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='usado', vin='AAAAAAAAAAAAAAAAB', patente='AB123CD', anio=2020, kilometraje=50000, procedencia='compra_directa')
        v.full_clean()

    def test_usado_sin_patente(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='usado', vin='AAAAAAAAAAAAAAAAC', anio=2020, kilometraje=50000, procedencia='compra_directa')
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_usado_kilometraje_cero(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='usado', vin='AAAAAAAAAAAAAAAAD', patente='AC123CD', anio=2020, kilometraje=0, procedencia='compra_directa')
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_usado_sin_procedencia(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='usado', vin='AAAAAAAAAAAAAAAAE', patente='AD123CD', anio=2020, kilometraje=50000)
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_anio_menor_a_1990(self):
        v = Vehiculo(**self.datos_base, condicion_vehiculo='usado', vin='AAAAAAAAAAAAAAAAF', patente='AE123CD', anio=1989, kilometraje=50000, procedencia='compra_directa')
        with self.assertRaises(DjangoValidationError):
            v.full_clean()

    def test_patente_duplicada(self):
        Vehiculo.objects.create(**self.datos_base, vin='AAAAAAAAAAAAAAAAG', condicion_vehiculo='usado', patente='AF123CD', anio=2020, kilometraje=50000, procedencia='compra_directa')
        v2 = Vehiculo(**self.datos_base, vin='AAAAAAAAAAAAAAAAH', condicion_vehiculo='usado', patente='AF123CD', anio=2019, kilometraje=30000, procedencia='compra_directa')
        with self.assertRaises(DjangoValidationError):
            v2.full_clean()

    def test_soft_delete_en_stock(self):
        v = Vehiculo.objects.create(**self.datos_base, condicion_vehiculo='0km', anio=2025, vin='DDDDDDDDDDDDDDDDD')
        v.soft_delete()
        self.assertFalse(Vehiculo.objects.filter(pk=v.pk).exists())

    def test_soft_delete_vendido_falla(self):
        v = Vehiculo.objects.create(**self.datos_base, condicion_vehiculo='0km', anio=2025, vin='EEEEEEEEEEEEEEEEE')
        v.estado = 'vendido'
        v.save(update_fields=['estado'])
        with self.assertRaises(DjangoValidationError):
            v.soft_delete()

    def test_soft_delete_reservado_falla(self):
        v = Vehiculo.objects.create(**self.datos_base, condicion_vehiculo='0km', anio=2025, vin='FFFFFFFFFFFFFFFFF')
        v.estado = 'reservado'
        v.save(update_fields=['estado'])
        with self.assertRaises(DjangoValidationError):
            v.soft_delete()

    def test_delete_fisico_no_permitido(self):
        v = Vehiculo.objects.create(**self.datos_base, condicion_vehiculo='0km', anio=2025, vin='GGGGGGGGGGGGGGGGG')
        with self.assertRaises(DjangoValidationError):
            v.delete()


class VehiculoUsadoSerializerTest(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='S', direccion='S', ciudad='S', provincia='S'
        )
        self.marca = Marca.objects.create(nombre="T2")
        self.modelo = Modelo.objects.create(
            nombre="C2", marca=self.marca, carroceria="sedan"
        )
        self.vehiculo_usado = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            color='blanco', precio_costo=10000, precio=12000,
            descripcion_tecnica='test',
            combustible='nafta', transmision='manual', puertas=4, motor='1.6',
            numero_serie_motor='MOTOR123', vin='USAD0123456789012',
            condicion_vehiculo='usado', patente='AB123CD',
            anio=2020, kilometraje=100, procedencia='compra_directa'
        )
        self.vehiculo_nuevo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            color='blanco', precio_costo=10000, precio=12000,
            descripcion_tecnica='test',
            combustible='nafta', transmision='manual', puertas=4, motor='1.6',
            numero_serie_motor='MOTOR456', vin='NUEV0123456789012',
            condicion_vehiculo='0km', anio=2026
        )

    def test_valida_condicion_usado(self):
        serializer = VehiculoUsadoSerializer(data={
            'vehiculo': self.vehiculo_nuevo.id,
            'precio_tasacion_final': 5000,
            'fecha_ingreso': '2026-06-28',
        })
        serializer.is_valid()
        with self.assertRaises(DRFValidationError):
            serializer.validate({'vehiculo': self.vehiculo_nuevo})

    def test_valida_taller_campos_requeridos(self):
        from inventario.models import Taller
        taller = Taller.objects.create(nombre='Taller Test')
        serializer = VehiculoUsadoSerializer()
        with self.assertRaises(DRFValidationError):
            serializer.validate({
                'vehiculo': self.vehiculo_usado,
                'taller': taller,
            })

    def test_valida_fecha_evaluacion_posterior_a_ingreso(self):
        from datetime import date
        serializer = VehiculoUsadoSerializer()
        with self.assertRaises(DRFValidationError):
            serializer.validate({
                'vehiculo': self.vehiculo_usado,
                'fecha_evaluacion': date(2026, 6, 28),
                'fecha_ingreso': date(2026, 6, 27),
            })