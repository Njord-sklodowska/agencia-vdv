import random
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from inventario.models import Vehiculo, VehiculoUsado, Taller

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga evaluaciones técnicas y talleres para vehículos usados'

    def quantize_decimal(self, value):
        """Fuerza un valor a ser Decimal con exactamente 2 decimales."""
        return Decimal(str(value)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    def handle(self, *args, **options):

        self.stdout.write(self.style.MIGRATE_LABEL("Iniciando carga de evaluaciones técnicas..."))

        # 1. Crear Talleres si no existen
        talleres_data = [
            {"nombre": "Taller Central Tucumán", "direccion": "Av. Mitre 123", "telefono": "381-4000001", "email": "contacto@tallercentral.com"},
            {"nombre": "Taller Norte", "direccion": "Ruta 38 Km 10", "telefono": "381-4000002", "email": "info@tallernorte.com"},
            {"nombre": "Taller Santiago", "direccion": "Calle Belgrano 456", "telefono": "385-4000003", "email": "servicios@tallersantiago.com"},
        ]
        
        talleres_objs = []
        for t_data in talleres_data:
            taller, created = Taller.objects.get_or_create(nombre=t_data['nombre'], defaults=t_data)
            talleres_objs.append(taller)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Taller creado: {taller.nombre}"))

        # 2. Obtener un usuario para autorizar
        try:
            usuario_autoriza = User.objects.first()
            if not usuario_autoriza:
                raise User.DoesNotExist
            self.stdout.write(self.style.SUCCESS(f"Usuario autorizador detectado: {usuario_autoriza.username}"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR("No se encontró ningún usuario en la base de datos. Por favor, crea un usuario antes de ejecutar este script."))
            return

        # 3. Buscar vehículos usados que NO tengan evaluación
        # Usamos all_objects para incluir los que puedan estar inactivos
        vehiculos_usados = Vehiculo.all_objects.filter(condicion_vehiculo='usado')
        
        # Filtrar los que ya tienen un VehiculoUsado asociado para evitar errores de OneToOneField
        usados_sin_evaluacion = [v for v in vehiculos_usados if not hasattr(v, 'vehiculo_usado')]

        if not usados_sin_evaluacion:
            self.stdout.write(self.style.WARNING("No se encontraron vehículos usados pendientes de evaluación."))
            return

        success_count = 0
        failure_count = 0
        
        estados_opciones = ['bueno', 'regular', 'malo']

        for vehiculo in usados_sin_evaluacion:
            try:
                # Calcular fechas coherentes (dentro de los últimos 30 días)
                # fecha_ingreso: hace entre 1 y 10 días
                dias_atras_ingreso = random.randint(1, 10)
                fecha_ingreso = date.today() - timedelta(days=dias_atras_ingreso)
                
                # fecha_evaluacion: debe ser <= fecha_ingreso y no más de 30 días atrás
                dias_atras_eval = random.randint(0, 2) # Evaluado entre 0 y 2 días antes del ingreso
                fecha_evaluacion = fecha_ingreso - timedelta(days=dias_atras_eval)

                # Precio de tasación: basado en el precio de costo del vehículo +/- 10%
                costo = float(vehiculo.precio_costo) if vehiculo.precio_costo else 10000.0
                tasacion_val = costo * random.uniform(0.9, 1.1)
                tasacion = self.quantize_decimal(tasacion_val)

                evaluacion = VehiculoUsado(
                    vehiculo=vehiculo,
                    taller=random.choice(talleres_objs),
                    usuario_autoriza=usuario_autoriza,
                    precio_info_auto=self.quantize_decimal(tasacion_val * 1.05),
                    porcentaje_deduccion=self.quantize_decimal(random.uniform(2.0, 15.0)),
                    precio_tasacion_final=tasacion,
                    estado_cubierta=random.choice(estados_opciones),
                    estado_motor=random.choice(estados_opciones),
                    estado_chapa_pintura=random.choice(estados_opciones),
                    estado_interior=random.choice(estados_opciones),
                    fecha_evaluacion=fecha_evaluacion,
                    fecha_ingreso=fecha_ingreso,
                    observaciones="Evaluación técnica estándar realizada en taller autorizado."
                )
                
                evaluacion.full_clean()
                evaluacion.save()
                
                self.stdout.write(self.style.SUCCESS(f"Evaluación creada para: {vehiculo}"))
                success_count += 1

            except ValidationError as e:
                self.stderr.write(self.style.ERROR(f"Error de validación en {vehiculo}: {e}"))
                failure_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error inesperado en {vehiculo}: {str(e)}"))
                failure_count += 1

        self.stdout.write(self.style.SUCCESS(f"\nProceso terminado: {success_count} evaluaciones creadas, {failure_count} fallidas."))
