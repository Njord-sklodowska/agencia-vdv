
from django.test import TestCase
from django.core.exceptions import ValidationError
from inventario.models import Vehiculo, Marca, Modelo
from sucursal.models import Sucursal


class VehiculoModelTest(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test',
            direccion='Test',
            ciudad='Test',
            provincia='Test'
        )

        self.marca = Marca.objects.create(nombre="Toyota")

        self.modelo = Modelo.objects.create(
            nombre="Corolla",
            marca=self.marca,
            carroceria="sedan"
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
            anio=2025,
            vin='AAAAAAAAAAAAAAAAA',
        )
        v.full_clean()

    def test_0km_no_puede_tener_patente(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
            patente='AA123BB',
            vin='BBBBBBBBBBBBBBBBB',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_0km_kilometraje_maximo_500(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
            kilometraje=501,
            vin='CCCCCCCCCCCCCCCCC',
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    def test_vin_invalido_con_letra_i(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='0km',
            vin='AAAAAAAAAAAAAAAAI',
            anio=2025,
        )
        with self.assertRaises(ValidationError):
            v.full_clean()

    # --- USADO ---

    def test_usado_valido(self):
        v = Vehiculo(
            **self.datos_base,
            condicion_vehiculo='usado',
            vin='AAAAAAAAAAAAAAAAB',
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
            vin='AAAAAAAAAAAAAAAAC',
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
            vin='AAAAAAAAAAAAAAAAD',
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
            vin='AAAAAAAAAAAAAAAAE',
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
            vin='AAAAAAAAAAAAAAAAF',
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
            vin='AAAAAAAAAAAAAAAAG',
            condicion_vehiculo='usado',
            patente='AF123CD',
            anio=2020,
            kilometraje=50000,
            procedencia='compra_directa',
        )
        v2 = Vehiculo(
            **self.datos_base,
            vin='AAAAAAAAAAAAAAAAH',
            condicion_vehiculo='usado',
            patente='AF123CD',
            anio=2019,
            kilometraje=30000,
            procedencia='compra_directa',
        )
        with self.assertRaises(ValidationError):
            v2.full_clean()

    # --- SOFT DELETE ---

    def test_soft_delete_en_stock(self):
        v = Vehiculo.objects.create(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
            vin='DDDDDDDDDDDDDDDDD', 
        )
        v.soft_delete()
        self.assertFalse(Vehiculo.objects.filter(pk=v.pk).exists())
        self.assertTrue(Vehiculo.all_objects.filter(pk=v.pk).exists())

    def test_soft_delete_vendido_falla(self):
        v = Vehiculo.objects.create(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
             vin='EEEEEEEEEEEEEEEEE', 
        )
        v.estado = 'vendido'
        v.save(skip_validation=True)
        with self.assertRaises(ValidationError):
            v.soft_delete()

    def test_soft_delete_reservado_falla(self):
        v = Vehiculo.objects.create(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
            vin='FFFFFFFFFFFFFFFFF', 
        )
        v.estado = 'reservado'
        v.save(skip_validation=True)
        with self.assertRaises(ValidationError):
            v.soft_delete()

    def test_delete_fisico_no_permitido(self):
        v = Vehiculo.objects.create(
            **self.datos_base,
            condicion_vehiculo='0km',
            anio=2025,
            vin='GGGGGGGGGGGGGGGGG', 
        )
        with self.assertRaises(ValidationError):
            v.delete()