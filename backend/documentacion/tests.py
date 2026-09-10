from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from inventario.models import Marca, Modelo, Vehiculo
from sucursal.models import Sucursal
from usuario.models import Rol

from .models import DocumentacionVehiculo, Gestor, TipoDocumento
from .serializers import DocumentacionVehiculoSerializer

User = get_user_model()


# ---------------------------------------------------------------------------
# Helpers compartidos
# ---------------------------------------------------------------------------

def crear_vehiculo(sucursal, marca, modelo, vin, patente=None, condicion='usado',
                    anio=2020, kilometraje=50000, procedencia='compra_directa'):
    """Arma un Vehiculo válido sin repetir todos sus campos obligatorios en cada test."""
    datos = dict(
        sucursal=sucursal, marca=marca, modelo=modelo,
        color='blanco', precio_costo=10000, precio=12000,
        descripcion_tecnica='test', combustible='nafta', transmision='manual',
        puertas=4, motor='1.6', numero_serie_motor=f'MOTOR-{vin}',
        vin=vin, condicion_vehiculo=condicion, anio=anio, kilometraje=kilometraje,
    )
    if patente:
        datos['patente'] = patente
    if condicion == 'usado':
        datos['procedencia'] = procedencia
    return Vehiculo.objects.create(**datos)


def crear_usuario_autenticado(client, username='tester', rol_nombre='Administrador'):
    """Crea un Rol + Usuario y lo autentica en el APIClient dado. Devuelve el Usuario."""
    rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)
    user = User.objects.create_user(
        username=username, password='testpass123',
        email=f'{username}@example.com', nombre='Test', apellido='User',
        rol=rol,
    )
    client.force_authenticate(user=user)
    return user


def obtener_resultados(data):
    """
    Devuelve la lista de resultados de una response, sea que el endpoint
    esté paginado (dict con 'results') o no (lista plana / ReturnList).
    Este proyecto no tiene paginación configurada globalmente, así que
    normalmente cae en la segunda rama — pero queda a prueba de que
    alguien la active más adelante.
    """
    if isinstance(data, dict):
        return data.get('results', data)
    return data


class BaseDocumentacionTestCase(TestCase):
    """Setup común: sucursal, marca/modelo, un vehículo, y cliente autenticado."""

    def setUp(self):
        self.client = APIClient()
        self.usuario = crear_usuario_autenticado(self.client)

        # La migración de datos precarga 12 TipoDocumento reales (todos
        # es_obligatorio=True) y también corre sobre la base de test. Si no
        # los neutralizamos acá, cualquier test que cuente "documentos
        # faltantes" los va a sumar además de los tipos que el propio test
        # crea, dando números inflados. Los desactivamos para que cada test
        # controle explícitamente qué tipos entran en el cálculo.
        TipoDocumento.objects.update(es_obligatorio=False, activo=False)

        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Test', direccion='Test', ciudad='Test', provincia='Test'
        )
        self.marca = Marca.objects.create(nombre='Toyota')
        self.modelo = Modelo.objects.create(nombre='Corolla', marca=self.marca, carroceria='sedan')
        self.vehiculo = crear_vehiculo(
            self.sucursal, self.marca, self.modelo, vin='DCTEST00000000001', patente='DT123AA',
        )


# ---------------------------------------------------------------------------
# TipoDocumento — modelo y API
# ---------------------------------------------------------------------------

class TipoDocumentoModelTest(TestCase):

    def test_str(self):
        tipo = TipoDocumento.objects.create(nombre='TipoBetaQA')
        self.assertEqual(str(tipo), 'TipoBetaQA')

    def test_defaults(self):
        tipo = TipoDocumento.objects.create(nombre='TipoGammaQA')
        self.assertTrue(tipo.es_obligatorio)
        self.assertFalse(tipo.requiere_vencimiento)
        self.assertTrue(tipo.activo)

    def test_nombre_duplicado_falla(self):
        TipoDocumento.objects.create(nombre='TipoAlfaQA')
        duplicado = TipoDocumento(nombre='TipoAlfaQA')
        with self.assertRaises(DjangoValidationError):
            duplicado.full_clean()


class TipoDocumentoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        crear_usuario_autenticado(self.client)
        self.tipo_activo = TipoDocumento.objects.create(nombre='TipoAlfaQA', activo=True)
        self.tipo_inactivo = TipoDocumento.objects.create(nombre='TipoInactivoQA', activo=False)

    def test_list_solo_muestra_activos(self):
        response = self.client.get('/api/documentacion/tipos-documento/')
        nombres = [t['nombre'] for t in obtener_resultados(response.data)]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('TipoAlfaQA', nombres)
        self.assertNotIn('TipoInactivoQA', nombres)

    def test_create(self):
        response = self.client.post('/api/documentacion/tipos-documento/', {
            'nombre': 'TipoDeltaQA', 'es_obligatorio': True, 'requiere_vencimiento': False,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TipoDocumento.objects.filter(nombre='TipoDeltaQA').exists())

    def test_create_nombre_duplicado_falla(self):
        response = self.client.post('/api/documentacion/tipos-documento/', {'nombre': 'TipoAlfaQA'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        response = self.client.get(f'/api/documentacion/tipos-documento/{self.tipo_activo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'TipoAlfaQA')

    def test_update_parcial(self):
        response = self.client.patch(
            f'/api/documentacion/tipos-documento/{self.tipo_activo.id}/',
            {'requiere_vencimiento': True},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo_activo.refresh_from_db()
        self.assertTrue(self.tipo_activo.requiere_vencimiento)

    def test_delete(self):
        response = self.client.delete(f'/api/documentacion/tipos-documento/{self.tipo_activo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TipoDocumento.objects.filter(id=self.tipo_activo.id).exists())

    def test_sin_autenticacion_rechazado(self):
        client_anonimo = APIClient()
        response = client_anonimo.get('/api/documentacion/tipos-documento/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# Gestor — modelo y API
# ---------------------------------------------------------------------------

class GestorModelTest(TestCase):

    def test_str_formato_apellido_coma_nombre(self):
        gestor = Gestor.objects.create(nombre='Carlos', apellido='Gomez', telefono='123')
        self.assertEqual(str(gestor), 'Gomez, Carlos')

    def test_estado_default_activo(self):
        gestor = Gestor.objects.create(nombre='Carlos', apellido='Gomez', telefono='123')
        self.assertEqual(gestor.estado, 'activo')


class GestorAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        crear_usuario_autenticado(self.client)
        self.gestor_activo = Gestor.objects.create(nombre='Carlos', apellido='Gomez', telefono='123', estado='activo')
        self.gestor_inactivo = Gestor.objects.create(nombre='Ana', apellido='Diaz', telefono='456', estado='inactivo')

    def test_list_solo_muestra_activos(self):
        response = self.client.get('/api/documentacion/gestores/')
        apellidos = [g['apellido'] for g in obtener_resultados(response.data)]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Gomez', apellidos)
        self.assertNotIn('Diaz', apellidos)

    def test_create(self):
        response = self.client.post('/api/documentacion/gestores/', {
            'nombre': 'Maria', 'apellido': 'Lopez', 'telefono': '789', 'email': 'mlopez@test.com',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        response = self.client.patch(
            f'/api/documentacion/gestores/{self.gestor_activo.id}/', {'telefono': '999'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.gestor_activo.refresh_from_db()
        self.assertEqual(self.gestor_activo.telefono, '999')

    def test_delete(self):
        response = self.client.delete(f'/api/documentacion/gestores/{self.gestor_activo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------------------
# DocumentacionVehiculo — modelo (RN-18 y comportamiento de relaciones)
# ---------------------------------------------------------------------------

class DocumentacionVehiculoModelTest(BaseDocumentacionTestCase):

    def setUp(self):
        super().setUp()
        self.tipo_titulo = TipoDocumento.objects.create(nombre='TipoAlfaQA', es_obligatorio=True, requiere_vencimiento=False)
        self.tipo_cedula = TipoDocumento.objects.create(nombre='TipoGammaQA', es_obligatorio=True, requiere_vencimiento=False)
        self.tipo_vtv = TipoDocumento.objects.create(nombre='TipoBetaQA', es_obligatorio=True, requiere_vencimiento=True)
        self.tipo_manual = TipoDocumento.objects.create(nombre='Manual', es_obligatorio=False, requiere_vencimiento=False)

    def test_str_documentacion_vehiculo(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, estado_documento='pendiente',
        )
        self.assertIn('TipoAlfaQA', str(doc))
        self.assertIn('DT123AA', str(doc))

    def test_str_usa_vin_si_no_hay_patente(self):
        vehiculo_0km = crear_vehiculo(
            self.sucursal, self.marca, self.modelo, vin='DCTEST00000000009', condicion='0km', kilometraje=0,
        )
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=vehiculo_0km, tipo_documento=self.tipo_titulo, estado_documento='pendiente',
        )
        self.assertIn('DCTEST00000000009', str(doc))

    def test_activo_default_true(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        self.assertTrue(doc.activo)

    def test_esta_vencido_true(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv, estado_documento='completado',
            fecha_vencimiento=date.today() - timedelta(days=1),
        )
        self.assertTrue(doc.esta_vencido)

    def test_esta_vencido_false_fecha_futura(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv, estado_documento='completado',
            fecha_vencimiento=date.today() + timedelta(days=1),
        )
        self.assertFalse(doc.esta_vencido)

    def test_esta_vencido_false_sin_fecha(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        self.assertFalse(doc.esta_vencido)

    def test_documento_no_iniciado_aparece_como_faltante(self):
        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        motivos = {f['tipo_documento']: f['motivo'] for f in faltantes}

        self.assertEqual(len(faltantes), 3)  # titulo, cedula, vtv (manual no es obligatorio)
        self.assertEqual(motivos['TipoAlfaQA'], 'no_iniciado')
        self.assertEqual(motivos['TipoGammaQA'], 'no_iniciado')
        self.assertEqual(motivos['TipoBetaQA'], 'no_iniciado')
        self.assertFalse(DocumentacionVehiculo.documentacion_completa(self.vehiculo))

    def test_documento_en_tramite_aparece_con_su_estado_como_motivo(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, estado_documento='en_tramite',
        )
        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        motivos = {f['tipo_documento']: f['motivo'] for f in faltantes}
        self.assertEqual(motivos['TipoAlfaQA'], 'en_tramite')

    def test_documento_completado_no_aparece_como_faltante(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        nombres_faltantes = [f['tipo_documento'] for f in faltantes]
        self.assertNotIn('TipoAlfaQA', nombres_faltantes)
        self.assertIn('TipoGammaQA', nombres_faltantes)

    def test_documento_completado_pero_vencido_aparece_como_faltante(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() - timedelta(days=5),
        )
        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        motivos = {f['tipo_documento']: f['motivo'] for f in faltantes}
        self.assertEqual(motivos['TipoBetaQA'], 'vencido')
        self.assertFalse(DocumentacionVehiculo.documentacion_completa(self.vehiculo))

    def test_documentacion_completa_true_cuando_todo_esta_completado_y_vigente(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_cedula,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() + timedelta(days=180),
        )
        self.assertEqual(DocumentacionVehiculo.documentos_faltantes(self.vehiculo), [])
        self.assertTrue(DocumentacionVehiculo.documentacion_completa(self.vehiculo))

    def test_documentacion_completa_true_sin_tipos_obligatorios(self):
        # Vehículo nuevo, sin ningún tipo obligatorio activo en el sistema.
        TipoDocumento.objects.all().update(es_obligatorio=False)
        otro_vehiculo = crear_vehiculo(
            self.sucursal, self.marca, self.modelo, vin='DCTEST00000000008', patente='ZY000ZY',
        )
        self.assertTrue(DocumentacionVehiculo.documentacion_completa(otro_vehiculo))

    def test_documento_mas_reciente_es_el_que_se_evalua(self):
        antiguo = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, estado_documento='pendiente',
        )
        antiguo.fecha_alta = date.today() - timedelta(days=10)
        antiguo.save(update_fields=['fecha_alta'])

        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        nombres_faltantes = [f['tipo_documento'] for f in faltantes]
        self.assertNotIn('TipoAlfaQA', nombres_faltantes)

    def test_documento_inactivo_no_cuenta_para_faltantes(self):
        # Un documento completado pero dado de baja (activo=False) no debe
        # "tapar" el faltante — para el sistema, es como si no existiera.
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        doc.activo = False
        doc.save(update_fields=['activo'])

        faltantes = DocumentacionVehiculo.documentos_faltantes(self.vehiculo)
        motivos = {f['tipo_documento']: f['motivo'] for f in faltantes}
        self.assertEqual(motivos['TipoAlfaQA'], 'no_iniciado')

    # -- Comportamiento de relaciones (on_delete) --

    def test_no_se_puede_borrar_vehiculo_con_documentos(self):
        # Vehiculo.delete() está sobreescrito en inventario/models.py para
        # bloquear siempre el borrado físico (no solo cuando hay documentos
        # asociados) — por eso acá esperamos DjangoValidationError, no el
        # ProtectedError que dispararía la FK on_delete=PROTECT si el
        # borrado físico llegara a intentarse.
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        with self.assertRaises(DjangoValidationError):
            self.vehiculo.delete()

    def test_borrar_gestor_no_borra_el_documento_solo_desvincula(self):
        gestor = Gestor.objects.create(nombre='Carlos', apellido='Gomez', telefono='123')
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, gestor=gestor,
        )
        gestor.delete()
        doc.refresh_from_db()
        self.assertIsNone(doc.gestor)
        self.assertTrue(DocumentacionVehiculo.objects.filter(id=doc.id).exists())

    def test_no_se_puede_borrar_tipo_documento_con_documentos(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        with self.assertRaises(ProtectedError):
            self.tipo_titulo.delete()


# ---------------------------------------------------------------------------
# DocumentacionVehiculo — serializer (todas las reglas de validate())
# ---------------------------------------------------------------------------

class DocumentacionVehiculoSerializerTest(BaseDocumentacionTestCase):

    def setUp(self):
        super().setUp()
        self.tipo_titulo = TipoDocumento.objects.create(nombre='TipoAlfaQA', es_obligatorio=True, requiere_vencimiento=False)
        self.tipo_vtv = TipoDocumento.objects.create(nombre='TipoBetaQA', es_obligatorio=True, requiere_vencimiento=True)
        self.gestor = Gestor.objects.create(nombre='Juan', apellido='Perez', telefono='3854000000', estado='activo')

    def _datos_base(self):
        return {
            'vehiculo': self.vehiculo.id,
            'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'pendiente',
        }

    # -- RN-19: gestor requiere fechas --

    def test_gestor_sin_fecha_entrega_ni_estimada_falla(self):
        data = self._datos_base()
        data['gestor'] = self.gestor.id
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_entrega_gestor', serializer.errors)
        self.assertIn('fecha_estimada_devolucion', serializer.errors)

    def test_gestor_solo_con_fecha_entrega_sigue_fallando(self):
        data = self._datos_base()
        data.update({'gestor': self.gestor.id, 'fecha_entrega_gestor': '2026-01-10'})
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_estimada_devolucion', serializer.errors)
        self.assertNotIn('fecha_entrega_gestor', serializer.errors)

    def test_gestor_con_ambas_fechas_es_valido(self):
        data = self._datos_base()
        data.update({
            'gestor': self.gestor.id,
            'fecha_entrega_gestor': '2026-01-10',
            'fecha_estimada_devolucion': '2026-01-20',
        })
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_sin_gestor_no_exige_fechas_de_gestoria(self):
        data = self._datos_base()
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # -- Coherencia de fechas --

    def test_fecha_estimada_anterior_a_entrega_falla(self):
        data = self._datos_base()
        data.update({
            'gestor': self.gestor.id,
            'fecha_entrega_gestor': '2026-01-20',
            'fecha_estimada_devolucion': '2026-01-10',
        })
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_estimada_devolucion', serializer.errors)

    def test_fecha_estimada_igual_a_entrega_es_valido(self):
        data = self._datos_base()
        data.update({
            'gestor': self.gestor.id,
            'fecha_entrega_gestor': '2026-01-20',
            'fecha_estimada_devolucion': '2026-01-20',
        })
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_fecha_real_anterior_a_entrega_falla(self):
        data = self._datos_base()
        data.update({
            'gestor': self.gestor.id,
            'fecha_entrega_gestor': '2026-01-20',
            'fecha_estimada_devolucion': '2026-01-25',
            'fecha_devolucion_real': '2026-01-15',
        })
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_devolucion_real', serializer.errors)

    # -- Recepción / completado --

    def test_estado_recibido_sin_fecha_recepcion_falla(self):
        data = self._datos_base()
        data['estado_documento'] = 'recibido'
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_recepcion', serializer.errors)

    def test_estado_pendiente_no_exige_fecha_recepcion(self):
        data = self._datos_base()
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_estado_completado_con_gestor_sin_fecha_devolucion_real_falla(self):
        data = self._datos_base()
        data.update({
            'estado_documento': 'completado',
            'fecha_recepcion': '2026-01-25',
            'gestor': self.gestor.id,
            'fecha_entrega_gestor': '2026-01-10',
            'fecha_estimada_devolucion': '2026-01-20',
        })
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_devolucion_real', serializer.errors)

    def test_estado_completado_sin_gestor_no_exige_fecha_devolucion_real(self):
        data = self._datos_base()
        data.update({'estado_documento': 'completado', 'fecha_recepcion': '2026-01-25'})
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # -- requiere_vencimiento --

    def test_tipo_con_requiere_vencimiento_sin_fecha_vencimiento_falla_al_completar(self):
        data = {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_vtv.id,
            'estado_documento': 'completado', 'fecha_recepcion': '2026-01-25',
        }
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('fecha_vencimiento', serializer.errors)

    def test_tipo_con_requiere_vencimiento_sin_completar_no_exige_fecha(self):
        data = {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_vtv.id,
            'estado_documento': 'en_tramite',
        }
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_tipo_con_requiere_vencimiento_y_fecha_vencimiento_es_valido(self):
        data = {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_vtv.id,
            'estado_documento': 'completado', 'fecha_recepcion': '2026-01-25',
            'fecha_vencimiento': '2027-01-25',
        }
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # -- Archivo PDF --

    def test_archivo_no_pdf_falla(self):
        archivo = SimpleUploadedFile('titulo.exe', b'contenido falso', content_type='application/octet-stream')
        data = self._datos_base()
        data['archivo_pdf'] = archivo
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('archivo_pdf', serializer.errors)

    def test_archivo_pdf_es_valido(self):
        archivo = SimpleUploadedFile('titulo.pdf', b'%PDF-1.4 contenido falso', content_type='application/pdf')
        data = self._datos_base()
        data['archivo_pdf'] = archivo
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_sin_archivo_es_valido(self):
        serializer = DocumentacionVehiculoSerializer(data=self._datos_base())
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # -- PATCH parcial --

    def test_patch_sin_tocar_fechas_no_reclama_lo_ya_guardado(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='en_tramite', gestor=self.gestor,
            fecha_entrega_gestor=date(2026, 1, 10), fecha_estimada_devolucion=date(2026, 1, 20),
        )
        serializer = DocumentacionVehiculoSerializer(
            instance=doc, data={'observaciones': 'seguimiento telefónico'}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_patch_que_avanza_estado_no_exige_retroactivamente_otros_campos(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, estado_documento='pendiente',
        )
        serializer = DocumentacionVehiculoSerializer(
            instance=doc, data={'estado_documento': 'en_tramite'}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

    # -- Campos read-only calculados --

    def test_nombre_gestor_null_si_no_hay_gestor(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        serializer = DocumentacionVehiculoSerializer(instance=doc)
        self.assertIsNone(serializer.data['nombre_gestor'])

    def test_nombre_gestor_combina_nombre_y_apellido(self):
        doc = DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, gestor=self.gestor,
            fecha_entrega_gestor=date.today(), fecha_estimada_devolucion=date.today() + timedelta(days=10),
        )
        serializer = DocumentacionVehiculoSerializer(instance=doc)
        self.assertEqual(serializer.data['nombre_gestor'], 'Juan Perez')

    def test_activo_no_editable_via_serializer(self):
        # Regresión: 'activo' debe ser read-only. Si alguien lo manda igual
        # en el payload, el serializer lo tiene que ignorar sin fallar.
        data = self._datos_base()
        data['activo'] = False
        serializer = DocumentacionVehiculoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('activo', serializer.validated_data)


# ---------------------------------------------------------------------------
# DocumentacionVehiculo — API completa (CRUD, filtros, acciones custom, permisos)
# ---------------------------------------------------------------------------

class DocumentacionVehiculoAPITest(BaseDocumentacionTestCase):

    def setUp(self):
        super().setUp()
        self.tipo_titulo = TipoDocumento.objects.create(nombre='TipoAlfaQA', es_obligatorio=True, requiere_vencimiento=False)
        self.tipo_vtv = TipoDocumento.objects.create(nombre='TipoBetaQA', es_obligatorio=True, requiere_vencimiento=True)
        self.gestor = Gestor.objects.create(nombre='Carlos', apellido='Gomez', telefono='123', estado='activo')

    # -- CRUD estándar --

    def test_create_json(self):
        response = self.client.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'pendiente',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get('/api/documentacion/documentacion-vehiculo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resultados = obtener_resultados(response.data)
        self.assertEqual(len(resultados), 1)

    def test_retrieve(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get(f'/api/documentacion/documentacion-vehiculo/{doc.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patente_vehiculo'], 'DT123AA')
        self.assertEqual(response.data['nombre_tipo_documento'], 'TipoAlfaQA')

    def test_retrieve_inexistente_404(self):
        response = self.client.get('/api/documentacion/documentacion-vehiculo/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_patch(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.patch(
            f'/api/documentacion/documentacion-vehiculo/{doc.id}/', {'estado_documento': 'en_tramite'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        doc.refresh_from_db()
        self.assertEqual(doc.estado_documento, 'en_tramite')

    def test_delete(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.delete(f'/api/documentacion/documentacion-vehiculo/{doc.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DocumentacionVehiculo.objects.filter(id=doc.id).exists())

    def test_create_con_datos_invalidos_devuelve_400_con_detalle(self):
        response = self.client.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'recibido',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fecha_recepcion', response.data)

    # -- Regresión específica del bug de 'activo' vía multipart --

    def test_create_multipart_sin_mandar_activo_queda_activo_true(self):
        response = self.client.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'pendiente',
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = DocumentacionVehiculo.objects.get(id=response.data['id'])
        self.assertTrue(doc.activo)

    def test_create_multipart_mandando_activo_false_no_lo_desactiva(self):
        response = self.client.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'pendiente', 'activo': 'false',
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        doc = DocumentacionVehiculo.objects.get(id=response.data['id'])
        self.assertTrue(doc.activo)

    def test_documento_desactivado_no_aparece_en_list(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        doc.activo = False
        doc.save(update_fields=['activo'])

        response = self.client.get('/api/documentacion/documentacion-vehiculo/')
        ids = [d['id'] for d in obtener_resultados(response.data)]
        self.assertNotIn(doc.id, ids)

    # -- Subida real de archivo --

    def test_create_con_archivo_pdf_real(self):
        archivo = SimpleUploadedFile('titulo.pdf', b'%PDF-1.4 contenido', content_type='application/pdf')
        response = self.client.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
            'estado_documento': 'pendiente', 'archivo_pdf': archivo,
        }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['archivo_pdf'])

    # -- Filtros por querystring --

    def test_filtro_por_vehiculo(self):
        otro_vehiculo = crear_vehiculo(self.sucursal, self.marca, self.modelo, vin='DCTEST00000000005', patente='ZZ999ZZ')
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        DocumentacionVehiculo.objects.create(vehiculo=otro_vehiculo, tipo_documento=self.tipo_titulo)

        response = self.client.get('/api/documentacion/documentacion-vehiculo/', {'vehiculo': self.vehiculo.id})
        resultados = obtener_resultados(response.data)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['vehiculo'], self.vehiculo.id)

    def test_filtro_por_estado_documento(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo, estado_documento='pendiente')
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv, estado_documento='completado',
            fecha_recepcion=date.today(), fecha_vencimiento=date.today() + timedelta(days=100),
        )

        response = self.client.get('/api/documentacion/documentacion-vehiculo/', {'estado_documento': 'completado'})
        resultados = obtener_resultados(response.data)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['estado_documento'], 'completado')

    def test_filtro_por_gestor(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv, gestor=self.gestor,
            fecha_entrega_gestor=date.today(), fecha_estimada_devolucion=date.today() + timedelta(days=10),
        )

        response = self.client.get('/api/documentacion/documentacion-vehiculo/', {'gestor': self.gestor.id})
        resultados = obtener_resultados(response.data)
        self.assertEqual(len(resultados), 1)

    def test_filtro_por_tipo_documento(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv)

        response = self.client.get('/api/documentacion/documentacion-vehiculo/', {'tipo_documento': self.tipo_vtv.id})
        resultados = obtener_resultados(response.data)
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]['tipo_documento'], self.tipo_vtv.id)

    # -- Acción custom: buscar --

    def test_buscar_por_patente(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get('/api/documentacion/documentacion-vehiculo/buscar/', {'q': 'DT123AA'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_buscar_por_patente_case_insensitive(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get('/api/documentacion/documentacion-vehiculo/buscar/', {'q': 'dt123aa'})
        self.assertEqual(len(response.data), 1)

    def test_buscar_por_vin(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get('/api/documentacion/documentacion-vehiculo/buscar/', {'q': 'DCTEST00000000001'})
        self.assertEqual(len(response.data), 1)

    def test_buscar_sin_resultados(self):
        response = self.client.get('/api/documentacion/documentacion-vehiculo/buscar/', {'q': 'NOEXISTE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_buscar_sin_query_param_falla(self):
        response = self.client.get('/api/documentacion/documentacion-vehiculo/buscar/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -- Acción custom: estado-vehiculo --

    def test_estado_vehiculo_incompleto(self):
        response = self.client.get(f'/api/documentacion/documentacion-vehiculo/estado-vehiculo/{self.vehiculo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['documentacion_completa'])
        self.assertEqual(len(response.data['documentos_faltantes']), 2)

    def test_estado_vehiculo_completo(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo,
            estado_documento='completado', fecha_recepcion=date.today(),
        )
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() + timedelta(days=90),
        )
        response = self.client.get(f'/api/documentacion/documentacion-vehiculo/estado-vehiculo/{self.vehiculo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['documentacion_completa'])
        self.assertEqual(response.data['documentos_faltantes'], [])

    def test_estado_vehiculo_inexistente_404(self):
        response = self.client.get('/api/documentacion/documentacion-vehiculo/estado-vehiculo/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # -- Acción custom: alertas-vencimiento --

    def test_alertas_vencimiento_incluye_proximos_a_vencer(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() + timedelta(days=10),
        )
        response = self.client.get('/api/documentacion/documentacion-vehiculo/alertas-vencimiento/', {'dias': 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_alertas_vencimiento_incluye_ya_vencidos(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() - timedelta(days=5),
        )
        response = self.client.get('/api/documentacion/documentacion-vehiculo/alertas-vencimiento/', {'dias': 30})
        self.assertEqual(len(response.data), 1)

    def test_alertas_vencimiento_no_incluye_los_lejanos(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() + timedelta(days=200),
        )
        response = self.client.get('/api/documentacion/documentacion-vehiculo/alertas-vencimiento/', {'dias': 30})
        self.assertEqual(len(response.data), 0)

    def test_alertas_vencimiento_no_incluye_sin_fecha_vencimiento(self):
        DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        response = self.client.get('/api/documentacion/documentacion-vehiculo/alertas-vencimiento/', {'dias': 30})
        self.assertEqual(len(response.data), 0)

    def test_alertas_vencimiento_usa_30_dias_por_defecto(self):
        DocumentacionVehiculo.objects.create(
            vehiculo=self.vehiculo, tipo_documento=self.tipo_vtv,
            estado_documento='completado', fecha_recepcion=date.today(),
            fecha_vencimiento=date.today() + timedelta(days=20),
        )
        response = self.client.get('/api/documentacion/documentacion-vehiculo/alertas-vencimiento/')
        self.assertEqual(len(response.data), 1)

    # -- Permisos --

    def test_list_sin_autenticacion_rechazado(self):
        client_anonimo = APIClient()
        response = client_anonimo.get('/api/documentacion/documentacion-vehiculo/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sin_autenticacion_rechazado(self):
        client_anonimo = APIClient()
        response = client_anonimo.post('/api/documentacion/documentacion-vehiculo/', {
            'vehiculo': self.vehiculo.id, 'tipo_documento': self.tipo_titulo.id,
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_sin_autenticacion_rechazado(self):
        doc = DocumentacionVehiculo.objects.create(vehiculo=self.vehiculo, tipo_documento=self.tipo_titulo)
        client_anonimo = APIClient()
        response = client_anonimo.delete(f'/api/documentacion/documentacion-vehiculo/{doc.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# Conexión real: obtener un JWT de verdad (no force_authenticate) y usarlo
# ---------------------------------------------------------------------------

class ConexionJWTTest(TestCase):
    """
    A diferencia del resto de los tests (que usan force_authenticate, un
    atajo de test que no pasa por el login real), esta clase valida el
    circuito completo: pedir un token con usuario/contraseña reales,
    y usarlo para autenticar una request a la API de documentación.
    """

    def setUp(self):
        self.rol = Rol.objects.create(nombre='Administrador')
        self.password = 'claveSegura123'
        self.usuario = User.objects.create_user(
            username='login_real', password=self.password,
            email='login_real@example.com', nombre='Test', apellido='User', rol=self.rol,
        )
        self.sucursal = Sucursal.objects.create(nombre='Sucursal Test', direccion='Test', ciudad='Test', provincia='Test')
        self.marca = Marca.objects.create(nombre='Toyota')
        self.modelo = Modelo.objects.create(nombre='Corolla', marca=self.marca, carroceria='sedan')
        self.vehiculo = crear_vehiculo(self.sucursal, self.marca, self.modelo, vin='DCTEST00000000007', patente='JW123AA')
        self.tipo_titulo = TipoDocumento.objects.create(nombre='TipoAlfaQA')

    def test_login_con_credenciales_correctas_devuelve_tokens(self):
        client = APIClient()
        response = client.post('/api/token/', {'username': 'login_real', 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_con_password_incorrecta_falla(self):
        client = APIClient()
        response = client.post('/api/token/', {'username': 'login_real', 'password': 'incorrecta'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_real_permite_acceder_a_documentacion(self):
        client = APIClient()
        login = client.post('/api/token/', {'username': 'login_real', 'password': self.password})
        access_token = login.data['access']

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = client.get('/api/documentacion/documentacion-vehiculo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sin_token_rechaza_acceso(self):
        client = APIClient()
        response = client.get('/api/documentacion/documentacion-vehiculo/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_devuelve_access_nuevo(self):
        client = APIClient()
        login = client.post('/api/token/', {'username': 'login_real', 'password': self.password})
        refresh_token = login.data['refresh']

        response = client.post('/api/token/refresh/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_invalido_rechazado(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer token-invalido-inventado')
        response = client.get('/api/documentacion/documentacion-vehiculo/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)