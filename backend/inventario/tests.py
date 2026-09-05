
from django.test import TestCase
from django.core.exceptions import ValidationError

from sucursal.models import Sucursal
from inventario.models import Marca, Modelo, Vehiculo


class VehiculoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Toyota')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Corolla', carroceria='sedan',
        )

    def _datos_base(self, **overrides):
        datos = dict(
            sucursal=self.sucursal,
            marca=self.marca,
            modelo=self.modelo,
            anio=2026,
            color='Blanco',
            precio_costo=15000000,
            precio=18000000,
            descripcion_tecnica='Test',
            combustible='nafta',
            transmision='manual',
            puertas=4,
            motor='1.6L',
            numero_serie_motor='MOT-TEST-0001',
        )
        datos.update(overrides)
        return datos

    # ---------- 0KM ----------

    def test_0km_valido_se_crea_correctamente(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633A004352',
            kilometraje=10,
        ))
        v.save()
        self.assertIsNotNone(v.pk)
        self.assertEqual(v.estado, 'en_stock')

    def test_0km_no_puede_superar_500km(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633A004353',
            kilometraje=600,
        ))
        with self.assertRaises(ValidationError):
            v.save()

    def test_0km_no_puede_tener_patente_en_stock(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633A004354',
            kilometraje=10,
            patente='ABC123',
            estado='en_stock',
        ))
        with self.assertRaises(ValidationError):
            v.save()

    # ---------- USADO ----------

    def test_usado_requiere_patente(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004355',
            kilometraje=50000,
            procedencia='compra_directa',
            # sin patente
        ))
        with self.assertRaises(ValidationError):
            v.save()

    def test_usado_requiere_kilometraje_mayor_a_cero(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004356',
            kilometraje=0,
            patente='ABC124',
            procedencia='compra_directa',
        ))
        with self.assertRaises(ValidationError):
            v.save()

    def test_usado_requiere_procedencia(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004357',
            kilometraje=50000,
            patente='ABC125',
            # sin procedencia
        ))
        with self.assertRaises(ValidationError):
            v.save()

    def test_usado_valido_se_crea_correctamente(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004358',
            kilometraje=50000,
            patente='ABC126',
            procedencia='compra_directa',
        ))
        v.save()
        self.assertIsNotNone(v.pk)

    # ---------- VIN Y PATENTE ----------

    def test_vin_con_letra_o_es_invalido(self):
        v = Vehiculo(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633AOO4352',  # tiene "O", prohibida
            kilometraje=10,
        ))
        with self.assertRaises(ValidationError):
            v.save()

    def test_patente_duplicada_no_permitida(self):
        Vehiculo.objects.create(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004359',
            kilometraje=50000,
            patente='ABC127',
            procedencia='compra_directa',
        ))
        v2 = Vehiculo(**self._datos_base(
            condicion_vehiculo='usado',
            vin='1HGCM82633A004360',
            kilometraje=30000,
            patente='ABC127',  # misma patente
            procedencia='parte_de_pago',
        ))
        with self.assertRaises(ValidationError):
            v2.save()

    # ---------- BORRADO ----------

    def test_no_permite_eliminar_fisicamente(self):
        v = Vehiculo.objects.create(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633A004361',
            kilometraje=10,
        ))
        with self.assertRaises(ValidationError):
            v.delete()

    def test_soft_delete_bloqueado_si_reservado(self):
        v = Vehiculo.objects.create(**self._datos_base(
            condicion_vehiculo='0km',
            vin='1HGCM82633A004362',
            kilometraje=10,
        ))
        v.estado = 'reservado'
        v.save(skip_validation=True)
        with self.assertRaises(ValidationError):
            v.soft_delete()

import datetime

from inventario.models import VehiculoUsado


class VehiculoUsadoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Ford')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Ranger', carroceria='pickup',
        )
        self.usuario = None  # se completa en cada test si hace falta

        from django.contrib.auth import get_user_model
        Usuario = get_user_model()
        self.usuario = Usuario.objects.create_user(
            username='autorizador_test', password='test12345'
        )

        self.vehiculo_usado_base = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='usado', vin='2HGCM82633A004400',
            anio=2018, color='Gris', precio_costo=1, precio=10000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='2.0L', numero_serie_motor='MOT-VU-0001',
            kilometraje=60000, patente='ABC900', procedencia='compra_directa',
        )

        self.vehiculo_0km_base = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='2HGCM82633A004401',
            anio=2026, color='Blanco', precio_costo=15000000, precio=18000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='2.0L', numero_serie_motor='MOT-VU-0002',
            kilometraje=10,
        )

    def _datos_base(self, **overrides):
        hoy = datetime.date.today()
        datos = dict(
            vehiculo=self.vehiculo_usado_base,
            usuario_autoriza=self.usuario,
            precio_tasacion_final=8000000,
            fecha_ingreso=hoy,
        )
        datos.update(overrides)
        return datos

    def test_no_se_puede_evaluar_vehiculo_0km(self):
        vu = VehiculoUsado(**self._datos_base(vehiculo=self.vehiculo_0km_base))
        with self.assertRaises(ValidationError):
            vu.save()

    def test_precio_tasacion_debe_ser_mayor_a_cero(self):
        vu = VehiculoUsado(**self._datos_base(precio_tasacion_final=0))
        with self.assertRaises(ValidationError):
            vu.save()

    def test_fecha_ingreso_no_puede_ser_futura(self):
        manana = datetime.date.today() + datetime.timedelta(days=1)
        vu = VehiculoUsado(**self._datos_base(fecha_ingreso=manana))
        with self.assertRaises(ValidationError):
            vu.save()

    def test_fecha_ingreso_no_puede_superar_30_dias(self):
        hace_40_dias = datetime.date.today() - datetime.timedelta(days=40)
        vu = VehiculoUsado(**self._datos_base(fecha_ingreso=hace_40_dias))
        with self.assertRaises(ValidationError):
            vu.save()

    def test_fecha_evaluacion_no_puede_ser_posterior_a_fecha_ingreso(self):
        hoy = datetime.date.today()
        ayer = hoy - datetime.timedelta(days=1)
        vu = VehiculoUsado(**self._datos_base(
            fecha_ingreso=ayer,
            fecha_evaluacion=hoy,  # posterior al ingreso
        ))
        with self.assertRaises(ValidationError):
            vu.save()

    def test_creacion_valida_actualiza_precio_costo_del_vehiculo(self):
        vu = VehiculoUsado(**self._datos_base(precio_tasacion_final=7500000))
        vu.save()

        self.vehiculo_usado_base.refresh_from_db()
        self.assertEqual(self.vehiculo_usado_base.precio_costo, 7500000)


from inventario.models import TrasladoVehiculo


class TrasladoVehiculoTestCase(TestCase):

    def setUp(self):
        self.sucursal_origen = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.sucursal_destino = Sucursal.objects.create(
            nombre='Del Valle Sur', direccion='Otra Calle 456',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Renault')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Logan', carroceria='sedan',
        )

        from django.contrib.auth import get_user_model
        Usuario = get_user_model()
        self.usuario = Usuario.objects.create_user(
            username='traslados_test', password='test12345'
        )

        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal_origen, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='3HGCM82633A004500',
            anio=2026, color='Blanco', precio_costo=15000000, precio=18000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='MOT-TR-0001',
            kilometraje=10,
        )

    def test_no_se_puede_trasladar_vehiculo_vendido(self):
        self.vehiculo.estado = 'vendido'
        self.vehiculo.save(skip_validation=True)

        traslado = TrasladoVehiculo(
            vehiculo=self.vehiculo,
            sucursal_origen=self.sucursal_origen,
            sucursal_destino=self.sucursal_destino,
            usuario_autoriza=self.usuario,
            usuario_registro=self.usuario,
            fecha_traslado=datetime.date.today(),
        )
        with self.assertRaises(ValidationError):
            traslado.save()

    def test_sucursal_origen_debe_coincidir_con_sucursal_actual_del_vehiculo(self):
        traslado = TrasladoVehiculo(
            vehiculo=self.vehiculo,
            sucursal_origen=self.sucursal_destino,  # mal a propósito
            sucursal_destino=self.sucursal_origen,
            usuario_autoriza=self.usuario)