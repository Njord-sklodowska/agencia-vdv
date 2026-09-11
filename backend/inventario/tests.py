
from django.test import TestCase
from django.core.exceptions import ValidationError
from sucursal.models import Sucursal
from inventario.models import Marca, Modelo, Vehiculo, Taller
from django.contrib.auth import get_user_model
import datetime
from inventario.models import VehiculoUsado
from rest_framework.test import APIClient


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


from rest_framework.test import APIClient


class PermisoMarcaTestCase(TestCase):

    def setUp(self):
        from usuario.models import Rol
        self.rol_vendedor = Rol.objects.create(nombre='vendedor')
        self.rol_admin = Rol.objects.create(nombre='administrativo')

        Usuario = get_user_model()
        self.vendedor = Usuario.objects.create_user(
            username='test_vendedor', password='test12345', rol=self.rol_vendedor
        )
        self.administrativo = Usuario.objects.create_user(
            username='test_admin', password='test12345', rol=self.rol_admin
        )
        self.client = APIClient()

    def test_vendedor_no_puede_crear_marca(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.post('/api/inventario/marcas/', {'nombre': 'MarcaTestVendedor'})
        self.assertEqual(response.status_code, 403)

    def test_administrativo_puede_crear_marca(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.post('/api/inventario/marcas/', {'nombre': 'MarcaTestAdmin'})
        self.assertEqual(response.status_code, 201)


class PermisosInventarioTestCase(TestCase):

    def setUp(self):
        from usuario.models import Rol
        self.rol_vendedor, _ = Rol.objects.get_or_create(nombre='vendedor')
        self.rol_admin, _ = Rol.objects.get_or_create(nombre='administrativo')
        self.rol_gerente, _ = Rol.objects.get_or_create(nombre='gerente')

        Usuario = get_user_model()
        self.vendedor = Usuario.objects.create_user(
            username='perm_vendedor', password='test12345', rol=self.rol_vendedor
        )
        self.administrativo = Usuario.objects.create_user(
            username='perm_admin', password='test12345', rol=self.rol_admin
        )
        self.gerente = Usuario.objects.create_user(
            username='perm_gerente', password='test12345', rol=self.rol_gerente
        )

        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Permisos', direccion='Calle X 1',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='MarcaPermiso')
        self.modelo_existente = Modelo.objects.create(
            marca=self.marca, nombre='ModeloPermiso', carroceria='sedan',
        )
        self.taller = Taller.objects.create(nombre='TallerPermiso')

        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo_existente,
            condicion_vehiculo='0km', vin='PERMTEST0000000X1',
            anio=2026, color='Gris', precio_costo=5000000, precio=6000000,
            descripcion_tecnica='Test permisos', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='PERM-0001',
            kilometraje=5,
        )

        self.client = APIClient()

    # ---------- Modelo ----------

    def test_vendedor_no_puede_crear_modelo(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.post('/api/inventario/modelos/', {
            'marca': self.marca.id, 'nombre': 'Nuevo', 'carroceria': 'sedan',
        })
        self.assertEqual(response.status_code, 403)

    def test_administrativo_puede_crear_modelo(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.post('/api/inventario/modelos/', {
            'marca': self.marca.id, 'nombre': 'Nuevo', 'carroceria': 'sedan',
        })
        self.assertEqual(response.status_code, 201)

    # ---------- Taller ----------

    def test_vendedor_no_puede_crear_taller(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.post('/api/inventario/talleres/', {'nombre': 'Taller Nuevo'})
        self.assertEqual(response.status_code, 403)

    def test_administrativo_puede_crear_taller(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.post('/api/inventario/talleres/', {'nombre': 'Taller Nuevo'})
        self.assertEqual(response.status_code, 201)

    # ---------- Vehiculo: lectura libre, escritura restringida ----------

    def test_vendedor_puede_ver_vehiculos(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.get('/api/inventario/vehiculos/')
        self.assertEqual(response.status_code, 200)

    def test_vendedor_no_puede_crear_vehiculo(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.post('/api/inventario/vehiculos/', {
            'sucursal': self.sucursal.id, 'marca': self.marca.id, 'modelo': self.modelo_existente.id,
            'condicion_vehiculo': '0km', 'vin': 'PERMTEST9999999X2',
            'anio': 2026, 'color': 'Blanco', 'precio_costo': 5000000, 'precio': 6000000,
            'descripcion_tecnica': 'Test', 'combustible': 'nafta', 'transmision': 'manual',
            'puertas': 4, 'motor': '1.6L', 'numero_serie_motor': 'PERM-0002', 'kilometraje': 5,
        })
        self.assertEqual(response.status_code, 403)

    def test_administrativo_puede_crear_vehiculo(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.post('/api/inventario/vehiculos/', {
            'sucursal': self.sucursal.id, 'marca': self.marca.id, 'modelo': self.modelo_existente.id,
            'condicion_vehiculo': '0km', 'vin': 'PERMTEST0000000X3',
            'anio': 2026, 'color': 'Blanco', 'precio_costo': 5000000, 'precio': 6000000,
            'descripcion_tecnica': 'Test', 'combustible': 'nafta', 'transmision': 'manual',
            'puertas': 4, 'motor': '1.6L', 'numero_serie_motor': 'PERM-0003', 'kilometraje': 5,
        })
        self.assertEqual(response.status_code, 201)

    def test_vendedor_no_puede_desactivar_vehiculo(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.post(f'/api/inventario/vehiculos/{self.vehiculo.id}/desactivar/')
        self.assertEqual(response.status_code, 403)

    # ---------- VehiculoUsado: Gerente o Superadministrador ----------

    def test_administrativo_no_puede_crear_vehiculo_usado(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.post('/api/inventario/vehiculos-usados/', {
            'vehiculo': self.vehiculo.id, 'usuario_autoriza': self.administrativo.id,
            'precio_tasacion_final': '4000000.00',
            'fecha_ingreso': datetime.date.today().isoformat(),
        })
        self.assertEqual(response.status_code, 403)

    def test_gerente_puede_crear_vehiculo_usado(self):
        vehiculo_usado_cond = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo_existente,
            condicion_vehiculo='usado', vin='PERMTEST444444X49',
            anio=2019, color='Gris', precio_costo=1, precio=4000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='PERM-0004',
            kilometraje=50000, patente='PRM001', procedencia='compra_directa',
        )
        self.client.force_authenticate(user=self.gerente)
        response = self.client.post('/api/inventario/vehiculos-usados/', {
            'vehiculo': vehiculo_usado_cond.id, 'usuario_autoriza': self.gerente.id,
            'precio_tasacion_final': '3500000.00',
            'fecha_ingreso': datetime.date.today().isoformat(),
        })
        self.assertEqual(response.status_code, 201)


class OcultamientoPrecioCostoTestCase(TestCase):

    def setUp(self):
        from usuario.models import Rol
        self.rol_vendedor, _ = Rol.objects.get_or_create(nombre='vendedor')
        self.rol_admin, _ = Rol.objects.get_or_create(nombre='administrativo')

        Usuario = get_user_model()
        self.vendedor = Usuario.objects.create_user(
            username='oculto_vendedor', password='test12345', rol=self.rol_vendedor
        )
        self.administrativo = Usuario.objects.create_user(
            username='oculto_admin', password='test12345', rol=self.rol_admin
        )

        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Oculto', direccion='Calle Y 1',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.vendedor.sucursal = self.sucursal
        self.vendedor.save()
        self.administrativo.sucursal = self.sucursal
        self.administrativo.save()

        self.marca = Marca.objects.create(nombre='MarcaOculto')
        self.modelo = Modelo.objects.create(marca=self.marca, nombre='ModeloOculto', carroceria='sedan')

        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='JCULTJTESTHHH999P',
            anio=2026, color='Negro', precio_costo=5000000, precio=6000000,
            descripcion_tecnica='Test oculto', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='OCULTO-0001',
            kilometraje=5,
        )

        self.client = APIClient()

    def test_vendedor_no_ve_precio_costo(self):
        self.client.force_authenticate(user=self.vendedor)
        response = self.client.get(f'/api/inventario/vehiculos/{self.vehiculo.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('precio_costo', response.data)
        self.assertIn('precio', response.data)  # el precio de venta sí debe verse

    def test_administrativo_si_ve_precio_costo(self):
        self.client.force_authenticate(user=self.administrativo)
        response = self.client.get(f'/api/inventario/vehiculos/{self.vehiculo.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('precio_costo', response.data)

    def test_vendedor_ve_vehiculos_en_stock_y_reservado_no_vendido(self):
        vehiculo_reservado = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='PCULTPTEST99999X4',
            anio=2026, color='Blanco', precio_costo=4000000, precio=5000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='OCULTO-0002',
            kilometraje=5, estado='reservado',
        )
        vehiculo_vendido = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='PCULTPTEST99999X3',
            anio=2026, color='Rojo', precio_costo=4500000, precio=5500000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='OCULTO-0003',
            kilometraje=5, estado='vendido',
        )

        self.client.force_authenticate(user=self.vendedor)
        response = self.client.get('/api/inventario/vehiculos/')
        ids_visibles = [v['id'] for v in response.data]

        self.assertIn(self.vehiculo.id, ids_visibles)  # en_stock
        self.assertIn(vehiculo_reservado.id, ids_visibles)  # reservado
        self.assertNotIn(vehiculo_vendido.id, ids_visibles)  # vendido, no debe verlo