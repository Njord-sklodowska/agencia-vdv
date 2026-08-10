from django.core.management.base import BaseCommand
from inventario.models import Vehiculo, Fotografia_Vehiculo

class Command(BaseCommand):
    help = 'Carga fotografías ficticias para los vehículos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("Iniciando carga de fotografías..."))
        
        vehiculos = Vehiculo.all_objects.all()
        success_count = 0
        
        for vehiculo in vehiculos:
            try:
                # Creamos una foto de portada y una secundaria
                # Nota: El archivo físicamente no existe, pero el registro en BD sí.
                # En producción, el usuario subiría la imagen real.
                
                # Foto 1: Portada
                Fotografia_Vehiculo.objects.create(
                    vehiculo=vehiculo,
                    archivo='vehiculos/placeholder_portada.jpg',
                    es_portada=True,
                    orden=1,
                    tamano_bytes=102400,
                    mime_type='image/jpeg'
                )
                
                # Foto 2: Secundaria
                Fotografia_Vehiculo.objects.create(
                    vehiculo=vehiculo,
                    archivo='vehiculos/placeholder_interior.jpg',
                    es_portada=False,
                    orden=2,
                    tamano_bytes=102400,
                    mime_type='image/jpeg'
                )
                
                success_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error cargando fotos para {vehiculo}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Se han creado fotografías para {success_count} vehículos."))
