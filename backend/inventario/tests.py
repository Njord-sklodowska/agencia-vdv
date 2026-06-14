# inventario/tests.py

from django.test import TestCase
from django.core.exceptions import ValidationError
from inventario.models import Vehiculo, Marca, Modelo
from sucursal.models import Sucursal

class VehiculoModelTest(TestCase):

    def setUp(self):
        self.sucursal = self.Sucursal.objects.create(nombre='Sucursal Test')
        self.marca = Marca.objects.create(nombre='Toyota')
        self.modelo = Modelo.objects.create(
            marca=self.marca,
            nombre='Corolla',
            carroceria='sedan'
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

    # --- 0KM ---

    def test_0km_valido(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            vin='AAAAAAAAAAAAAAAAA',  # 17 chars válidos
            anio=2025,
        )
        v.full_clean()  # no debe lanzar error

    def test_0km_no_puede_tener_patente(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            vin='BBBBBBBBBBBBBBBBB',
            anio=2025,
            patente='AA123BB',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_0km_kilometraje_maximo_500(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            vin='CCCCCCCCCCCCCCCCC',
            anio=2025,
            kilometraje=501,
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_vin_invalido_con_letra_i(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            vin='AAAAAAAAAAAAAAAAI',  # contiene I
            anio=2025,
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    # --- USADO ---

    def test_usado_valido(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AB123CD',
            anio=2020,
            kilometraje=50000,
            procedencia='compra_directa',
        )
        v.full_clean()

    def test_usado_sin_patente(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            anio=2020,
            kilometraje=50000,
            procedencia='compra_directa',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_usado_kilometraje_cero(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AC123CD',
            anio=2020,
            kilometraje=0,
            procedencia='compra_directa',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_usado_sin_procedencia(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AD123CD',
            anio=2020,
            kilometraje=50000,
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    # --- AÑO ---

    def test_anio_menor_a_1990(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AE123CD',
            anio=1989,
            kilometraje=50000,
            procedencia='compra_directa',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    # --- PATENTE DUPLICADA ---

    def test_patente_duplicada(self):
        Vehiculo.objects.create(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AF123CD',
            anio=2020,
            kilometraje=50000,
            procedencia='compra_directa',
        )
        v2 = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            patente='AF123CD',
            anio=2019,
            kilometraje=30000,
            procedencia='compra_directa',
        )
        with self.assertRaises(ValidationError):
            v2.full_clean()