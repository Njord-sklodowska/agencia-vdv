import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from clientes.models import Cliente

class Command(BaseCommand):
    help = 'Carga clientes de prueba (Físicos y Jurídicos) para el sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_LABEL("Iniciando carga de clientes de prueba..."))

        # Datos para generar personas físicas
        nombres = ["Juan", "María", "Pedro", "Ana", "Luis", "Lucía", "Carlos", "Elena", "Jorge", "Sofía"]
        apellidos = ["García", "Rodríguez", "López", "Martínez", "González", "Sánchez", "Pérez", "Gómez", "Fernández", "Díaz"]
        ciudades = ["San Miguel", "Concepción", "Banda", "Tucumán", "Yerba Buena"]
        calles = ["Av. Mitre", "Calle Belgrano", "Av. Alem", "Calle San Martín", "Av. Colombia"]
        iva_opciones = ["responsable_inscripto", "monotributista", "consumidor_final"]
        cuil_prefijos = ["20", "23", "24", "27"]

        # Datos para generar personas jurídicas
        razones_sociales = [
            "Transportes del Norte S.A.", "Autopartes Global S.R.L.", "Logística Express S.A.S.", 
            "Inversiones Automotrices S.A.", "Servicios Mecánicos Industriales S.R.L.", 
            "Consorcio Vial del Norte", "Importadora de Lujo S.A."
        ]
        fantasias = ["TransNorte", "GlobalParts", "ExpressLog", "InvAuto", "MecInd", "ConsorVial", "LuxeImport"]

        success_count = 0
        failure_count = 0

        # 1. Generar Personas Físicas (20 clientes)
        for i in range(20):
            try:
                nombre = random.choice(nombres)
                apellido = random.choice(apellidos)
                # DNI: 8 dígitos - generar DNI válido
                dni = f"{random.randint(20, 45)}{random.randint(100000, 999999)}"
                # CUIL: 11 dígitos (prefijo + DNI + verificador)
                prefijo = random.choice(cuil_prefijos)
                verificador = random.randint(0, 9)
                cuil = f"{prefijo}{dni}{verificador}"
                
                cliente = Cliente(
                    tipo_persona='fisica',
                    dni_cuit=dni,
                    cuil=cuil,
                    condicion_iva=random.choice(iva_opciones),
                    nombre=nombre,
                    apellido=apellido,
                    telefono=f"381{random.randint(1000000, 9999999)}",
                    domicilio_real=f"{random.choice(calles)} {random.randint(100, 2000)}, {random.choice(ciudades)}",
                    fecha_nacimiento=date.today() - timedelta(days=random.randint(6570, 18250)), # Entre 18 y 50 años
                    estado='activo'
                )
                cliente.full_clean()
                cliente.save()
                success_count += 1
            except ValidationError as e:
                self.stderr.write(self.style.ERROR(f"Error de validación en persona física {i+1}: {e}"))
                failure_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error inesperado en persona física {i+1}: {str(e)}"))
                failure_count += 1

        # 2. Generar Personas Jurídicas (10 clientes)
        cuit_prefijos = ["30", "33", "34"]
        for i in range(len(razones_sociales)):
            try:
                # CUIT: 11 dígitos (prefijo 30/33/34 + 8 dígitos + verificador)
                prefijo = random.choice(cuit_prefijos)
                cuit = f"{prefijo}{random.randint(10000000, 99999999)}{random.randint(0, 9)}"
                
                cliente = Cliente(
                    tipo_persona='juridica',
                    dni_cuit=cuit,
                    razon_social=razones_sociales[i],
                    nombre_fantasia=fantasias[i],
                    condicion_iva="responsable_inscripto",
                    telefono=f"3814{random.randint(1000000, 9999999)}",
                    domicilio_real=f"{random.choice(calles)} {random.randint(100, 2000)}, {random.choice(ciudades)}",
                    estado='activo'
                )
                cliente.full_clean()
                cliente.save()
                success_count += 1
            except ValidationError as e:
                self.stderr.write(self.style.ERROR(f"Error de validación en persona jurídica {i+1}: {e}"))
                failure_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error inesperado en persona jurídica {i+1}: {str(e)}"))
                failure_count += 1

        self.stdout.write(self.style.SUCCESS(f"\nCarga de clientes finalizada: {success_count} exitosos, {failure_count} fallidos."))
