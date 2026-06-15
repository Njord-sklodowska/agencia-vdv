import json
import sys
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from inventario.models import Marca, Modelo, Vehiculo
from sucursal.models import Sucursal

class Command(BaseCommand):
    help = 'Carga masiva de vehículos desde un archivo JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Ruta al archivo JSON con los datos de los vehículos')

    def handle(self, *args, **options):
        json_file = options['json_file']

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Archivo no encontrado: {json_file}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"Error al decodificar el JSON en {json_file}"))
            return

        if not isinstance(data, list):
            self.stderr.write(self.style.ERROR("El archivo JSON debe contener una lista de vehículos."))
            return

        success_count = 0
        failure_count = 0

        for index, item in enumerate(data):
            try:
                # Resolver Sucursal
                sucursal_nombre = item.get('sucursal', '').strip()
                if not sucursal_nombre:
                    raise ValidationError("Falta el nombre de la sucursal")
                
                # Búsqueda insensible a mayúsculas/minúsculas
                try:
                    sucursal = Sucursal.objects.get(nombre__iexact=sucursal_nombre)
                except Sucursal.DoesNotExist:
                    # Intentamos buscar una sucursal que contenga el nombre si la coincidencia exacta falla
                    sucursales_similares = Sucursal.objects.filter(nombre__icontains=sucursal_nombre)
                    if sucursales_similares.exists():
                        sucursal = sucursales_similares.first()
                        self.stdout.write(self.style.WARNING(f"[{index+1}] Nota: No se encontró '{sucursal_nombre}' exactamente. Usando sucursal similar: '{sucursal.nombre}'"))
                    else:
                        raise Sucursal.DoesNotExist


                # Resolver Marca
                marca_nombre = item.get('marca')
                if not marca_nombre:
                    raise ValidationError("Falta el nombre de la marca")
                marca, created = Marca.objects.get_or_create(nombre=marca_nombre)

                # Resolver Modelo
                modelo_nombre = item.get('modelo')
                carroceria = item.get('carroceria')
                if not modelo_nombre:
                    raise ValidationError("Falta el nombre del modelo")
                if not carroceria:
                    raise ValidationError("Falta la carrocería para el modelo")
                
                modelo, created = Modelo.objects.get_or_create(
                    marca=marca, 
                    nombre=modelo_nombre, 
                    defaults={'carroceria': carroceria}
                )

                # Crear Vehículo
                # Extraemos los datos del vehículo excluyendo los que ya resolvimos como objetos
                vehiculo_data = {k: v for k, v in item.items() if k not in ['sucursal', 'marca', 'modelo', 'carroceria']}
                
                # Asignar las relaciones
                vehiculo_data['sucursal'] = sucursal
                vehiculo_data['marca'] = marca
                vehiculo_data['modelo'] = modelo

                vehiculo = Vehiculo(**vehiculo_data)
                
                # Ejecutar validaciones del modelo (full_clean llama a clean())
                vehiculo.full_clean()
                vehiculo.save()
                
                self.stdout.write(self.style.SUCCESS(f"[{index+1}] Vehículo cargado con éxito: {vehiculo}"))
                success_count += 1

            except Sucursal.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"[{index+1}] Error: Sucursal '{item.get('sucursal')}' no existe."))
                failure_count += 1
            except ValidationError as e:
                self.stderr.write(self.style.ERROR(f"[{index+1}] Error de validación: {e}"))
                failure_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"[{index+1}] Error inesperado: {str(e)}"))
                failure_count += 1

        self.stdout.write(self.style.SUCCESS(f"\nCarga finalizada: {success_count} exitosos, {failure_count} fallidos."))
