from django.db import migrations

# (nombre, es_obligatorio, requiere_vencimiento)
# 'Titulo' y 'VTV' se escriben exactamente igual que los ya cargados a mano
# durante las pruebas, para que get_or_create los reutilice en vez de
# crear un duplicado por una tilde de más o de menos.
TIPOS_DOCUMENTO = [
    ("08", True, False),
    ("Titulo", True, False),
    ("Cedula", True, False),
    ("Informe de Dominio", True, False),
    ("Informe de Multas", True, True),
    ("Patentes", True, False),
    ("Verificacion", True, False),
    ("F12", True, False),
    ("VTV", True, True),
    ("Prenda", True, False),
    ("Manuales", True, False),
    ("Duplicados de Llave", True, False),
]


def crear_tipos_documento(apps, schema_editor):
    TipoDocumento = apps.get_model("documentacion", "TipoDocumento")
    for nombre, es_obligatorio, requiere_vencimiento in TIPOS_DOCUMENTO:
        TipoDocumento.objects.get_or_create(
            nombre=nombre,
            defaults={
                "es_obligatorio": es_obligatorio,
                "requiere_vencimiento": requiere_vencimiento,
                "activo": True,
            },
        )


def eliminar_tipos_documento(apps, schema_editor):
    TipoDocumento = apps.get_model("documentacion", "TipoDocumento")
    TipoDocumento.objects.filter(
        nombre__in=[nombre for nombre, _, _ in TIPOS_DOCUMENTO]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("documentacion", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(crear_tipos_documento, eliminar_tipos_documento),
    ]
