import datetime
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ventas.models import FormaPago
from sucursal.models import Sucursal
from inventario.models import Marca, Modelo, Vehiculo
from clientes.models import Cliente
from ventas.models import OperacionVenta

Usuario = get_user_model()


class OperacionVentaTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Toyota')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Corolla', carroceria='sedan',
        )
        self.vendedor = Usuario.objects.create_user(
            username='vendedor_test', password='test12345'
        )

        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30123456789', cuil='20123456781',
            condicion_iva='consumidor_final', nombre='Juan', apellido='Pérez',
            telefono='2611234567', domicilio_real='Calle 1 123',
        )
        self.cliente_2 = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30123456790', cuil='20123456782',
            condicion_iva='consumidor_final', nombre='Ana', apellido='López',
            telefono='2611234568', domicilio_real='Calle 2 456',
        )

        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='4HGCM82633A004600',
            anio=2026, color='Blanco', precio_costo=15000000, precio=18000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='MOT-OV-0001',
            kilometraje=10,
        )

    def _datos_base(self, **overrides):
        datos = dict(
            sucursal=self.sucursal,
            cliente=self.cliente,
            vehiculo_vendido=self.vehiculo,
            vendedor=self.vendedor,
            usuario_registro=self.vendedor,
            fecha_operacion=datetime.date.today(),
        )
        datos.update(overrides)
        return datos

    def test_operacion_valida_se_crea_y_calcula_precio_final(self):
        op = OperacionVenta(**self._datos_base())
        op.save()
        self.assertEqual(op.precio_original, self.vehiculo.precio)
        self.assertEqual(op.precio_final, self.vehiculo.precio)
        self.assertEqual(op.estado, 'borrador')

    def test_cotitular_no_puede_ser_igual_a_titular(self):
        op = OperacionVenta(**self._datos_base(cliente_cotitular=self.cliente))
        with self.assertRaises(ValidationError):
            op.save()

    def test_no_se_puede_vender_vehiculo_ya_vendido(self):
        self.vehiculo.estado = 'vendido'
        self.vehiculo.save(skip_validation=True)

        op = OperacionVenta(**self._datos_base())
        with self.assertRaises(ValidationError):
            op.save()

    def test_no_permite_operacion_activa_duplicada_para_mismo_vehiculo(self):
        OperacionVenta.objects.create(**self._datos_base())

        op2 = OperacionVenta(**self._datos_base(cliente=self.cliente_2))
        with self.assertRaises(ValidationError):
            op2.save()

    def test_no_se_puede_confirmar_directamente_cambiando_estado(self):
        op = OperacionVenta.objects.create(**self._datos_base())
        op.estado = 'confirmada'
        with self.assertRaises(ValidationError):
            op.save()

    def test_no_se_puede_revertir_confirmada_a_borrador(self):
        op = OperacionVenta.objects.create(**self._datos_base())
        op.estado = 'confirmada'
        op.save(skip_validation=True)

        op.estado = 'borrador'
        with self.assertRaises(ValidationError):
            op.save()

    def test_cancelada_requiere_observaciones(self):
        op = OperacionVenta.objects.create(**self._datos_base())
        op.estado = 'cancelada'
        with self.assertRaises(ValidationError):
            op.save()

    def test_descuento_no_puede_superar_precio_original(self):
        op = OperacionVenta(**self._datos_base(
            descuento_aplicado=self.vehiculo.precio + 1000000,
        ))
        with self.assertRaises(ValidationError):
            op.save()
class AnticipoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Renault')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Logan', carroceria='sedan',
        )
        self.usuario = Usuario.objects.create_user(
            username='anticipo_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30999888777', cuil='20999888771',
            condicion_iva='consumidor_final', nombre='Marta', apellido='Gómez',
            telefono='2611112233', domicilio_real='Calle 3 789',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='5HGCM82633A004700',
            anio=2026, color='Negro', precio_costo=12000000, precio=15000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='MOT-AN-0001',
            kilometraje=5,
        )

    def _datos_base(self, **overrides):
        from ventas.models import Anticipo
        datos = dict(
            vehiculo=self.vehiculo,
            cliente=self.cliente,
            usuario_registro=self.usuario,
            monto=500000,
            forma_pago='efectivo',
            fecha_anticipo=datetime.date.today(),
        )
        datos.update(overrides)
        return datos

    def test_anticipo_valido_reserva_el_vehiculo(self):
        from ventas.models import Anticipo
        anticipo = Anticipo(**self._datos_base())
        anticipo.save()

        self.vehiculo.refresh_from_db()
        self.assertEqual(self.vehiculo.estado, 'reservado')

    def test_monto_cero_o_negativo_invalido(self):
        from ventas.models import Anticipo
        anticipo = Anticipo(**self._datos_base(monto=0))
        with self.assertRaises(ValidationError):
            anticipo.save()

    def test_estado_devuelto_requiere_observaciones(self):
        from ventas.models import Anticipo
        anticipo = Anticipo(**self._datos_base(estado='devuelto'))
        with self.assertRaises(ValidationError):
            anticipo.save()

    def test_fecha_anticipo_no_puede_ser_futura(self):
        from ventas.models import Anticipo
        manana = datetime.date.today() + datetime.timedelta(days=1)
        anticipo = Anticipo(**self._datos_base(fecha_anticipo=manana))
        with self.assertRaises(ValidationError):
            anticipo.save()

    def test_fecha_anticipo_no_puede_superar_30_dias(self):
        from ventas.models import Anticipo
        hace_40_dias = datetime.date.today() - datetime.timedelta(days=40)
        anticipo = Anticipo(**self._datos_base(fecha_anticipo=hace_40_dias))
        with self.assertRaises(ValidationError):
            anticipo.save()

    def test_no_se_puede_registrar_anticipo_sobre_vehiculo_no_disponible(self):
        from ventas.models import Anticipo
        self.vehiculo.estado = 'vendido'
        self.vehiculo.save(skip_validation=True)

        anticipo = Anticipo(**self._datos_base())
        with self.assertRaises(ValidationError):
            anticipo.save()

class FormaPagoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Nissan')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Sentra', carroceria='sedan',
        )
        self.usuario = Usuario.objects.create_user(
            username='formapago_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30777666555', cuil='20777666551',
            condicion_iva='consumidor_final', nombre='Luis', apellido='Diaz',
            telefono='2613334455', domicilio_real='Calle 5 111',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='6HGCM82633A004800',
            anio=2026, color='Gris', precio_costo=14000000, precio=17000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='MOT-FP-0001',
            kilometraje=5,
        )
        self.operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )

    def _datos_base(self, **overrides):
        from ventas.models import FormaPago
        datos = dict(
            operacion=self.operacion,
            tipo_pago='efectivo',
            monto=1000000,
        )
        datos.update(overrides)
        return datos

    def test_forma_pago_valida_se_crea_correctamente(self):
        from ventas.models import FormaPago
        fp = FormaPago(**self._datos_base())
        fp.save()
        self.assertIsNotNone(fp.pk)

    def test_dolares_requiere_cotizacion(self):
        from ventas.models import FormaPago
        fp = FormaPago(**self._datos_base(tipo_pago='dolares'))
        with self.assertRaises(ValidationError):
            fp.save()

    def test_no_dolares_no_debe_tener_cotizacion(self):
        from ventas.models import FormaPago
        fp = FormaPago(**self._datos_base(tipo_pago='efectivo', cotizacion_dolar=1000))
        with self.assertRaises(ValidationError):
            fp.save()

    def test_dolares_con_cotizacion_se_crea_correctamente(self):
        from ventas.models import FormaPago
        fp = FormaPago(**self._datos_base(tipo_pago='dolares', cotizacion_dolar=1000))
        fp.save()
        self.assertIsNotNone(fp.pk)


class TituloCreditoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Ford')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Ranger', carroceria='pickup',
        )
        self.usuario = Usuario.objects.create_user(
            username='titulo_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30555444333', cuil='20555444331',
            condicion_iva='consumidor_final', nombre='Pedro', apellido='Sosa',
            telefono='2615556677', domicilio_real='Calle 7 222',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='7HGCM82633A004900',
            anio=2026, color='Rojo', precio_costo=20000000, precio=24000000,
            descripcion_tecnica='Test', combustible='diesel', transmision='manual',
            puertas=4, motor='3.2L', numero_serie_motor='MOT-TC-0001',
            kilometraje=5,
        )
        self.operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )

        from ventas.models import FormaPago
        self.forma_pago_cheque = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='cheque', monto=5000000,
        )
        self.forma_pago_pagare = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='pagare', monto=3000000,
        )

    def _datos_cheque(self, **overrides):
        datos = dict(
            forma_pago=self.forma_pago_cheque,
            tipo='cheque',
            numero_documento='12345678',
            banco_emisor='Banco Nación',
            plazo_dias=30,
            fecha_recepcion=datetime.date.today(),
            monto=5000000,
        )
        datos.update(overrides)
        return datos

    def _datos_pagare(self, **overrides):
        datos = dict(
            forma_pago=self.forma_pago_pagare,
            tipo='pagare',
            numero_documento='PAG001',
            fecha_vencimiento_manual=datetime.date.today() + datetime.timedelta(days=60),
            fecha_recepcion=datetime.date.today(),
            monto=3000000,
        )
        datos.update(overrides)
        return datos

    def test_cheque_valido_calcula_fecha_cobro(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_cheque())
        t.save()
        self.assertEqual(t.fecha_cobro, t.fecha_recepcion + datetime.timedelta(days=30))

    def test_cheque_requiere_banco_emisor(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_cheque(banco_emisor=None))
        with self.assertRaises(ValidationError):
            t.save()

    def test_pagare_requiere_fecha_vencimiento_manual(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_pagare(fecha_vencimiento_manual=None))
        with self.assertRaises(ValidationError):
            t.save()

    def test_pagare_no_admite_plazo_dias(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_pagare(plazo_dias=30))
        with self.assertRaises(ValidationError):
            t.save()

    def test_no_puede_referenciar_forma_pago_y_anticipo_juntos(self):
        from ventas.models import TituloCredito, Anticipo
        anticipo = Anticipo.objects.create(
            vehiculo=self.vehiculo, cliente=self.cliente, usuario_registro=self.usuario,
            monto=1000000, forma_pago='efectivo', fecha_anticipo=datetime.date.today(),
        )
        t = TituloCredito(**self._datos_cheque(anticipo=anticipo))
        with self.assertRaises(ValidationError):
            t.save()

    def test_no_puede_dejar_ambos_vacios(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_cheque(forma_pago=None))
        with self.assertRaises(ValidationError):
            t.save()

    def test_numero_documento_duplicado_mismo_banco_no_permitido(self):
        from ventas.models import TituloCredito
        TituloCredito.objects.create(**self._datos_cheque())

        from ventas.models import FormaPago
        otra_forma_pago = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='cheque', monto=1000000,
        )
        t2 = TituloCredito(**self._datos_cheque(
            forma_pago=otra_forma_pago,
            numero_documento='12349876',  # mismo número
            banco_emisor='Banco Nación',  # mismo banco
        ))
        with self.assertRaises(ValidationError):
            t2.save()

    def test_rechazado_requiere_observaciones(self):
        from ventas.models import TituloCredito
        t = TituloCredito(**self._datos_cheque(estado='rechazado'))
        with self.assertRaises(ValidationError):
            t.save()
from django.db.utils import IntegrityError

class RegistroCobroTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Chevrolet')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Camaro', carroceria='coupe',
        )
        self.usuario = Usuario.objects.create_user(
            username='cobro_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30222333444', cuil='20222333441',
            condicion_iva='consumidor_final', nombre='Sofía', apellido='Ruiz',
            telefono='2617778899', domicilio_real='Calle 9 333',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='8HGCM82633A005000',
            anio=2026, color='Amarillo', precio_costo=30000000, precio=36000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='automatica',
            puertas=2, motor='6.2L', numero_serie_motor='MOT-RC-0001',
            kilometraje=5,
        )
        self.operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )
        from ventas.models import FormaPago, TituloCredito
        self.forma_pago_cheque = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='cheque', monto=8000000,
        )
        self.titulo_cheque = TituloCredito.objects.create(
            forma_pago=self.forma_pago_cheque, tipo='cheque',
            numero_documento='12345655', banco_emisor='Banco Galicia',
            plazo_dias=0, fecha_recepcion=datetime.date.today(), monto=8000000,
        )

        self.forma_pago_pagare = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='pagare', monto=4000000,
        )
        self.titulo_pagare = TituloCredito.objects.create(
            forma_pago=self.forma_pago_pagare, tipo='pagare',
            numero_documento='12345600', 
            titular='Juan Pérez',
            fecha_vencimiento_manual=datetime.date.today() + datetime.timedelta(days=30),
            fecha_recepcion=datetime.date.today(), 
            monto=4000000,
        )

    def test_cobro_de_cheque_marca_titulo_como_cobrado(self):
        from ventas.models import RegistroCobro
        rc = RegistroCobro(
            titulo=self.titulo_cheque, usuario_registro=self.usuario,
            fecha_pago_real=datetime.date.today(), monto_pagado=8000000,
            forma_cobro='cheque', forma_acreditacion_cheque='ventanilla',
        )
        rc.save()

        self.titulo_cheque.refresh_from_db()
        self.assertEqual(self.titulo_cheque.estado, 'cobrado')
        self.assertEqual(self.titulo_cheque.forma_acreditacion, 'ventanilla')

    def test_cheque_requiere_forma_acreditacion(self):
        from ventas.models import RegistroCobro
        rc = RegistroCobro(
            titulo=self.titulo_cheque, usuario_registro=self.usuario,
            fecha_pago_real=datetime.date.today(), monto_pagado=8000000,
            forma_cobro='cheque',
        )
        with self.assertRaises(ValidationError):
            rc.save()

    def test_pago_con_mora_requiere_pagare_vencido(self):
        from ventas.models import RegistroCobro
        # titulo_pagare está en estado 'pendiente', no 'vencido'
        rc = RegistroCobro(
            titulo=self.titulo_pagare, usuario_registro=self.usuario,
            fecha_pago_real=datetime.date.today(), monto_pagado=4000000,
            forma_cobro='pagare', pago_con_mora=True,
        )
        with self.assertRaises(ValidationError):
            rc.save()

    def test_pago_con_mora_valido_si_pagare_vencido(self):
        from ventas.models import RegistroCobro
        self.titulo_pagare.estado = 'vencido'
        self.titulo_pagare.save(skip_validation=True)

        rc = RegistroCobro(
            titulo=self.titulo_pagare, usuario_registro=self.usuario,
            fecha_pago_real=datetime.date.today(), monto_pagado=4000000,
            forma_cobro='pagare', pago_con_mora=True, monto_mora_pagado=50000,
        )
        rc.save()
        self.assertIsNotNone(rc.pk)

    def test_fecha_pago_no_puede_ser_futura(self):
        from ventas.models import RegistroCobro
        manana = datetime.date.today() + datetime.timedelta(days=1)
        rc = RegistroCobro(
            titulo=self.titulo_cheque, usuario_registro=self.usuario,
            fecha_pago_real=manana, monto_pagado=8000000,
            forma_cobro='cheque', forma_acreditacion_cheque='deposito',
        )
        with self.assertRaises(ValidationError):
            rc.save()


class CreditoInternoTestCase(TestCase):

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Volkswagen')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='Gol', carroceria='hatchback',
        )
        self.usuario = Usuario.objects.create_user(
            username='credito_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30111222333', cuil='20111222331',
            condicion_iva='consumidor_final', nombre='Carla', apellido='Vega',
            telefono='2619990011', domicilio_real='Calle 11 444',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='9HGCM82633A005100',
            anio=2026, color='Azul', precio_costo=10000000, precio=12000000,
            descripcion_tecnica='Test', combustible='nafta', transmision='manual',
            puertas=5, motor='1.6L', numero_serie_motor='MOT-CI-0001',
            kilometraje=5,
        )
        self.operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )

        
        self.forma_pago_credito = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='financiamiento_interno', monto=6000000,
        )
        self.forma_pago_efectivo = FormaPago.objects.create(
            operacion=self.operacion, tipo_pago='efectivo', monto=1000000,
        )

    def _datos_base(self, **overrides):
        datos = dict(
            operacion=self.operacion,
            forma_pago=self.forma_pago_credito,
            monto_financiado=6000000,
            cantidad_cuotas=6,
            tasa_interes_mensual=Decimal('5.00'),
            fecha_primera_cuota=datetime.date.today() + datetime.timedelta(days=30),
        )
        datos.update(overrides)
        return datos

    def test_credito_valido_calcula_monto_cuota_y_genera_cuotas(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno(**self._datos_base())
        credito.save()

        # monto_financiado * (1 + tasa/100 * cuotas) / cuotas
        esperado = (Decimal('6000000') * (1 + Decimal('5.00') / 100 * 6)) / 6
        esperado = esperado.quantize(Decimal('0.01'))

        self.assertEqual(credito.monto_cuota, esperado)
        self.assertEqual(credito.monto_total, esperado * 6)
        self.assertEqual(credito.cuotas.count(), 6)

    def test_cuotas_tienen_numeracion_correlativa_y_fechas_mensuales(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno.objects.create(**self._datos_base())

        cuotas = list(credito.cuotas.order_by('numero_cuota'))
        numeros = [c.numero_cuota for c in cuotas]
        self.assertEqual(numeros, [1, 2, 3, 4, 5, 6])

        # cada cuota vence un mes después de la anterior
        for i in range(1, len(cuotas)):
            diferencia_dias = (cuotas[i].fecha_vencimiento - cuotas[i - 1].fecha_vencimiento).days
            self.assertTrue(27 <= diferencia_dias <= 31)

    def test_forma_pago_debe_ser_tipo_financiamiento_interno(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno(**self._datos_base(forma_pago=self.forma_pago_efectivo))
        with self.assertRaises(ValidationError):
            credito.save()

    def test_cantidad_cuotas_debe_ser_mayor_a_cero(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno(**self._datos_base(cantidad_cuotas=0))
        with self.assertRaises(ValidationError):
            credito.save()

    def test_no_se_pueden_repetir_numero_cuota_en_mismo_credito(self):
        from ventas.models import CreditoInterno, CuotaCredito
        credito = CreditoInterno.objects.create(**self._datos_base())

        cuota_duplicada = CuotaCredito(
            credito_interno=credito, numero_cuota=1,  # ya existe la cuota 1
            monto_cuota=credito.monto_cuota,
            fecha_vencimiento=datetime.date.today(),
        )
        with self.assertRaises(Exception):
            cuota_duplicada.save()

    def test_marcar_cuota_pagada_requiere_datos_de_pago(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno.objects.create(**self._datos_base())
        cuota = credito.cuotas.first()

        cuota.estado = 'pagada'
        # sin monto_pagado, fecha_pago_real, forma_pago_cuota
        with self.assertRaises(ValidationError):
            cuota.save()

    def test_pagar_todas_las_cuotas_completa_el_credito(self):
        from ventas.models import CreditoInterno
        credito = CreditoInterno.objects.create(**self._datos_base(cantidad_cuotas=2))

        for cuota in credito.cuotas.order_by('numero_cuota'):
            cuota.estado = 'pagada'
            cuota.monto_pagado = cuota.monto_cuota
            cuota.fecha_pago_real = datetime.date.today()
            cuota.forma_pago_cuota = 'efectivo'
            cuota.save()

        credito.refresh_from_db()
        self.assertEqual(credito.estado, 'completado')

class CalculosFinancierosEdgeCasesTestCase(TestCase):
    """
    Casos borde de validaciones cruzadas y cálculos financieros:
    intereses de mora, cuotas de crédito interno, conversión de dólares,
    y desalineación de montos entre documentos relacionados.
    """

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Del Valle Centro', direccion='Calle Falsa 123',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Peugeot')
        self.modelo = Modelo.objects.create(
            marca=self.marca, nombre='208', carroceria='hatchback',
        )
        self.usuario = Usuario.objects.create_user(
            username='edge_test', password='test12345'
        )
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30444555666', cuil='20444555661',
            condicion_iva='consumidor_final', nombre='Edge', apellido='Case',
            telefono='2614445566', domicilio_real='Calle Edge 1',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='EDGCASE00000000X1',
            anio=2026, color='Negro', precio_costo=8000000, precio=10000000,
            descripcion_tecnica='Test edge', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='EDGE-0001',
            kilometraje=5,
        )
        self.operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )

    # ---------- Conversión de dólares ----------

    def test_forma_pago_dolares_sin_cotizacion_falla(self):
        from ventas.models import FormaPago
        fp = FormaPago(operacion=self.operacion, tipo_pago='dolares', monto=1000)
        with self.assertRaises(ValidationError):
            fp.save()

    def test_forma_pago_no_dolares_con_cotizacion_falla(self):
        from ventas.models import FormaPago
        fp = FormaPago(
            operacion=self.operacion, tipo_pago='efectivo', monto=1000,
            cotizacion_dolar=Decimal('1000.00'),
        )
        with self.assertRaises(ValidationError):
            fp.save()

    def test_forma_pago_dolares_con_cotizacion_cero_falla(self):
        from ventas.models import FormaPago
        # cotizacion_dolar=0 es "falsy" en Python: debe seguir exigiendo cotización real
        fp = FormaPago(
            operacion=self.operacion, tipo_pago='dolares', monto=1000,
            cotizacion_dolar=Decimal('0.00'),
        )
        with self.assertRaises(ValidationError):
            fp.save()

    # ---------- Desalineación de montos: TituloCredito vs FormaPago ----------

    def test_titulo_monto_desalineado_de_forma_pago_falla(self):
        from ventas.models import FormaPago, TituloCredito
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='cheque', monto=Decimal('300000.00'))
        titulo = TituloCredito(
            forma_pago=fp, tipo='cheque', numero_documento='11223344',
            banco_emisor='Banco Test', plazo_dias=30,
            fecha_recepcion=datetime.date.today(), monto=Decimal('299999.99'),  # 1 centavo de diferencia
        )
        with self.assertRaises(ValidationError):
            titulo.save()

    def test_titulo_tipo_no_coincide_con_forma_pago_falla(self):
        from ventas.models import FormaPago, TituloCredito
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='pagare', monto=Decimal('300000.00'))
        titulo = TituloCredito(
            forma_pago=fp, tipo='cheque',  # tipo distinto al de la forma de pago
            numero_documento='11223345', banco_emisor='Banco Test', plazo_dias=30,
            fecha_recepcion=datetime.date.today(), monto=Decimal('300000.00'),
        )
        with self.assertRaises(ValidationError):
            titulo.save()

    # ---------- Interés de mora ----------

    def test_pago_con_mora_en_pagare_no_vencido_falla(self):
        from ventas.models import FormaPago, TituloCredito, RegistroCobro
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='pagare', monto=Decimal('200000.00'))
        titulo = TituloCredito.objects.create(
            forma_pago=fp, tipo='pagare', numero_documento='PAGEDGE01', titular='Cliente Edge',
            fecha_vencimiento_manual=datetime.date.today() + datetime.timedelta(days=30),
            fecha_recepcion=datetime.date.today(), monto=Decimal('200000.00'),
        )
        # titulo.estado sigue en 'pendiente', no 'vencido'
        rc = RegistroCobro(
            titulo=titulo, usuario_registro=self.usuario,
            fecha_pago_real=datetime.date.today(), monto_pagado=Decimal('200000.00'),
            forma_cobro='pagare', pago_con_mora=True, monto_mora_pagado=Decimal('5000.00'),
        )
        with self.assertRaises(ValidationError):
            rc.save()

    def test_interes_mora_en_cheque_falla(self):
        from ventas.models import FormaPago, TituloCredito
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='cheque', monto=Decimal('200000.00'))
        titulo = TituloCredito(
            forma_pago=fp, tipo='cheque', numero_documento='11223346',
            banco_emisor='Banco Test', plazo_dias=30,
            fecha_recepcion=datetime.date.today(), monto=Decimal('200000.00'),
            interes_mora=Decimal('500.00'),  # no debería aplicar a cheques
        )
        with self.assertRaises(ValidationError):
            titulo.save()

    # ---------- Cuotas de crédito interno: cálculo y casos borde ----------

    def test_credito_interno_cuotas_cero_falla(self):
        from ventas.models import FormaPago, CreditoInterno
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='financiamiento_interno', monto=Decimal('500000.00'))
        credito = CreditoInterno(
            operacion=self.operacion, forma_pago=fp,
            monto_financiado=Decimal('500000.00'), cantidad_cuotas=0,
            tasa_interes_mensual=Decimal('5.00'),
            fecha_primera_cuota=datetime.date.today() + datetime.timedelta(days=30),
        )
        with self.assertRaises(ValidationError):
            credito.save()

    def test_credito_interno_monto_financiado_cero_falla(self):
        with self.assertRaises((ValidationError, IntegrityError)):
            FormaPago.objects.create(
                operacion=self.operacion, 
                tipo_pago='financiamiento_interno', 
                monto=Decimal('0.00')
            )

    def test_credito_interno_calculo_cuota_con_tasa_decimal_no_redonda(self):
        """
        Verifica que el cálculo de cuota siempre quede en exactamente 2 decimales,
        incluso con una tasa que produce divisiones no exactas (caso borde de redondeo).
        """
        from ventas.models import FormaPago, CreditoInterno
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='financiamiento_interno', monto=Decimal('333333.00'))
        credito = CreditoInterno.objects.create(
            operacion=self.operacion, forma_pago=fp,
            monto_financiado=Decimal('333333.00'), cantidad_cuotas=7,  # división no redonda
            tasa_interes_mensual=Decimal('3.33'),
            fecha_primera_cuota=datetime.date.today() + datetime.timedelta(days=30),
        )
        _, digits, exponent = credito.monto_cuota.as_tuple()
        self.assertEqual(exponent, -2)  # exactamente 2 decimales, sin errores de redondeo
        self.assertEqual(credito.cuotas.count(), 7)

    def test_cuota_marcada_pagada_sin_estado_explicito_falla(self):
        """
        Caso borde: se cargan los datos de pago pero no se marca el estado como
        'pagada' -> debe bloquear (regla agregada para evitar pagos no confirmados).
        """
        from ventas.models import FormaPago, CreditoInterno
        fp = FormaPago.objects.create(operacion=self.operacion, tipo_pago='financiamiento_interno', monto=Decimal('300000.00'))
        credito = CreditoInterno.objects.create(
            operacion=self.operacion, forma_pago=fp,
            monto_financiado=Decimal('300000.00'), cantidad_cuotas=3,
            tasa_interes_mensual=Decimal('5.00'),
            fecha_primera_cuota=datetime.date.today() + datetime.timedelta(days=30),
        )
        cuota = credito.cuotas.first()
        cuota.monto_pagado = cuota.monto_cuota
        cuota.fecha_pago_real = datetime.date.today()
        cuota.forma_pago_cuota = 'efectivo'
        # estado sigue en 'pendiente' -> debe fallar
        with self.assertRaises(ValidationError):
            cuota.save()

    # ---------- Confirmar operación con montos desalineados (caso borde central) ----------

    def test_confirmar_operacion_con_suma_formas_pago_desalineada(self):
        """
        Caso borde solicitado explícitamente: intentar confirmar una venta
        con la suma de formas de pago desalineada respecto al precio_final.
        """
        from ventas.models import FormaPago
        FormaPago.objects.create(operacion=self.operacion, tipo_pago='efectivo', monto=Decimal('9999999.99'))
        # precio_final de self.operacion es 10000000.00 -> desalineado por 1 centavo

        from rest_framework.test import APIClient
        client = APIClient()
        client.force_authenticate(user=self.usuario)
        response = client.post(f'/api/ventas/operaciones/{self.operacion.id}/confirmar/')
        self.assertEqual(response.status_code, 400)
        self.assertIn('no coincide', str(response.data))

class PrecioOriginalSnapshotTestCase(TestCase):
    """
    Prueba el fix: precio_original se fija solo al crear la operación,
    y no se pisa silenciosamente si el precio del vehículo cambia después
    (incluyendo guardados con skip_validation=True, como los que usan
    confirmar/cancelar/completar en el viewset).
    """

    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Snapshot', direccion='Calle Snap 1',
            ciudad='Mendoza', provincia='Mendoza',
        )
        self.marca = Marca.objects.create(nombre='Fiat')
        self.modelo = Modelo.objects.create(marca=self.marca, nombre='Cronos', carroceria='sedan')
        self.usuario = Usuario.objects.create_user(username='snapshot_test', password='test12345')
        self.cliente = Cliente.objects.create(
            tipo_persona='fisica', dni_cuit='30666777888', cuil='20666777881',
            condicion_iva='consumidor_final', nombre='Nico', apellido='Snap',
            telefono='2618889900', domicilio_real='Calle Snap 2',
        )
        self.vehiculo = Vehiculo.objects.create(
            sucursal=self.sucursal, marca=self.marca, modelo=self.modelo,
            condicion_vehiculo='0km', vin='SNAPTEST0000000X1',
            anio=2026, color='Gris', precio_costo=7000000, precio=9000000,
            descripcion_tecnica='Test snapshot', combustible='nafta', transmision='manual',
            puertas=4, motor='1.6L', numero_serie_motor='SNAP-0001',
            kilometraje=5,
        )

    def test_precio_original_no_cambia_si_el_vehiculo_cambia_de_precio_despues(self):
        from ventas.models import OperacionVenta

        operacion = OperacionVenta.objects.create(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )
        precio_original_al_crear = operacion.precio_original
        self.assertEqual(precio_original_al_crear, self.vehiculo.precio)  # 9000000

        # El precio del vehículo cambia DESPUÉS de crear la operación
        self.vehiculo.precio = Decimal('12000000')
        self.vehiculo.save(skip_validation=True)

        # Simulamos exactamente lo que hace confirmar()/cancelar()/completar(): skip_validation=True
        operacion.estado = 'confirmada'
        operacion.save(skip_validation=True)

        operacion.refresh_from_db()
        self.assertEqual(operacion.precio_original, precio_original_al_crear)  # sigue en 9000000
        self.assertNotEqual(operacion.precio_original, self.vehiculo.precio)  # no se pisó con 12000000

    def test_precio_original_se_fija_correctamente_al_crear(self):
        from ventas.models import OperacionVenta

        operacion = OperacionVenta(
            sucursal=self.sucursal, cliente=self.cliente,
            vehiculo_vendido=self.vehiculo, vendedor=self.usuario,
            usuario_registro=self.usuario, fecha_operacion=datetime.date.today(),
        )
        operacion.save()
        self.assertEqual(operacion.precio_original, self.vehiculo.precio)