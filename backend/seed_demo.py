from datetime import date, timedelta

from sucursal.models import Sucursal
from inventario.models import Marca, Modelo, Vehiculo
from documentacion.models import TipoDocumento, Gestor, DocumentacionVehiculo

sucursal = Sucursal.objects.first()
hoy = date.today()


def get_marca(nombre):
    m, _ = Marca.objects.get_or_create(nombre=nombre)
    return m


def get_modelo(marca, nombre, carroceria='sedan'):
    mo, _ = Modelo.objects.get_or_create(nombre=nombre, marca=marca, defaults={'carroceria': carroceria})
    return mo


def crear_vehiculo(marca_nombre, modelo_nombre, vin, patente, anio, km, color, precio, carroceria='sedan'):
    marca = get_marca(marca_nombre)
    modelo = get_modelo(marca, modelo_nombre, carroceria)
    v, _ = Vehiculo.objects.get_or_create(
        vin=vin,
        defaults=dict(
            sucursal=sucursal, marca=marca, modelo=modelo, color=color,
            precio_costo=precio * 0.8, precio=precio,
            descripcion_tecnica=f'{modelo_nombre} {anio}',
            combustible='nafta', transmision='manual', puertas=4, motor='1.6',
            numero_serie_motor=f'MOTOR-{vin}',
            condicion_vehiculo='usado', patente=patente, anio=anio,
            kilometraje=km, procedencia='compra_directa',
        )
    )
    return v


v2 = crear_vehiculo('Ford', 'Focus', 'FRDFCS20260000001', 'AC456EF', 2021, 42000, 'Gris', 12500000)
v3 = crear_vehiculo('Chevrolet', 'Onix', 'CHEVNX20260000002', 'AD789GH', 2022, 28000, 'Rojo', 11800000)
v4 = crear_vehiculo('Volkswagen', 'Gol', 'VWKSGN20260000003', 'AE321JK', 2020, 55000, 'Blanco', 9500000)
v5 = crear_vehiculo('Fiat', 'Cronos', 'FTCRNS20260000004', 'AF654LM', 2023, 12000, 'Negro', 13200000)

gestor1, _ = Gestor.objects.get_or_create(
    nombre='Carlos', apellido='Gomez',
    defaults={'telefono': '3854123456', 'email': 'cgomez@gestoria.com'}
)
gestor2, _ = Gestor.objects.get_or_create(
    nombre='Maria', apellido='Lopez',
    defaults={'telefono': '3854987654', 'email': 'mlopez@gestoria.com'}
)

tipos = {t.nombre: t for t in TipoDocumento.objects.all()}


def doc(vehiculo, tipo_nombre, estado, gestor=None, vencimiento=None):
    tipo = tipos[tipo_nombre]
    DocumentacionVehiculo.objects.get_or_create(
        vehiculo=vehiculo, tipo_documento=tipo,
        defaults=dict(
            estado_documento=estado, gestor=gestor,
            fecha_recepcion=hoy if estado in ['recibido', 'completado'] else None,
            fecha_entrega_gestor=hoy - timedelta(days=5) if gestor else None,
            fecha_estimada_devolucion=hoy + timedelta(days=10) if gestor else None,
            fecha_devolucion_real=hoy if (estado == 'completado' and gestor) else None,
            fecha_vencimiento=vencimiento,
        )
    )


# Ford Focus: gestor Maria, buen avance general
doc(v2, 'Titulo', 'completado', gestor2)
doc(v2, '08', 'completado', gestor2)
doc(v2, 'Cedula', 'en_tramite', gestor2)
doc(v2, 'VTV', 'completado', gestor2, vencimiento=hoy + timedelta(days=200))
doc(v2, 'Informe de Multas', 'pendiente', gestor2)

# Chevrolet Onix: gestor Carlos, recien arrancando
doc(v3, 'Titulo', 'pendiente', gestor1)
doc(v3, 'VTV', 'pendiente', gestor1)

# Volkswagen Gol: gestor Maria, documentacion casi completa (para mostrar RN-18)
doc(v4, 'Titulo', 'completado', gestor2)
doc(v4, '08', 'completado', gestor2)
doc(v4, 'Cedula', 'completado', gestor2)
doc(v4, 'Patentes', 'completado', gestor2)
doc(v4, 'Verificacion', 'completado', gestor2)
doc(v4, 'F12', 'completado', gestor2)
doc(v4, 'VTV', 'completado', gestor2, vencimiento=hoy + timedelta(days=300))
doc(v4, 'Informe de Multas', 'completado', gestor2, vencimiento=hoy + timedelta(days=300))
doc(v4, 'Informe de Dominio', 'completado', gestor2)

# Fiat Cronos: gestor Carlos, en trámite variado
doc(v5, 'Titulo', 'en_tramite', gestor1)
doc(v5, 'Cedula', 'recibido', gestor1)
doc(v5, 'VTV', 'en_tramite', gestor1)

print('Datos de demo cargados con exito')
print('Vehiculos:', Vehiculo.objects.count())
print('Documentos:', DocumentacionVehiculo.objects.count())
print('Gestores:', Gestor.objects.count())