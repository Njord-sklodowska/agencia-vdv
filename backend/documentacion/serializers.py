from rest_framework import serializers

from .models import DocumentacionVehiculo, Gestor, TipoDocumento


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = "__all__"


class GestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestor
        fields = "__all__"


class DocumentacionVehiculoSerializer(serializers.ModelSerializer):
    nombre_tipo_documento = serializers.ReadOnlyField(source="tipo_documento.nombre")
    patente_vehiculo = serializers.ReadOnlyField(source="vehiculo.patente")
    nombre_gestor = serializers.SerializerMethodField()
    esta_vencido = serializers.ReadOnlyField()

    class Meta:
        model = DocumentacionVehiculo
        fields = "__all__"
        # 'activo' nunca debe llegar desde el cliente: DRF trata los
        # BooleanField ausentes en multipart/form-data como checkboxes sin
        # marcar (los interpreta como False), ignorando el default=True del
        # modelo. Como la baja lógica debería hacerse con una acción propia
        # (no exponiéndola como campo editable), la marcamos read-only.
        read_only_fields = ["activo", "fecha_alta", "updated_at"]

    def get_nombre_gestor(self, obj):
        if obj.gestor:
            return f"{obj.gestor.nombre} {obj.gestor.apellido}"
        return None

    def validate_archivo_pdf(self, value):
        if value and not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("El archivo adjunto debe ser en formato PDF.")
        return value

    def _valor(self, data, campo):
        """Devuelve el valor entrante o, si no vino (PATCH), el valor actual de la instancia."""
        if campo in data:
            return data[campo]
        return getattr(self.instance, campo, None)

    def validate(self, data):
        gestor = self._valor(data, "gestor")
        fecha_entrega_gestor = self._valor(data, "fecha_entrega_gestor")
        fecha_estimada = self._valor(data, "fecha_estimada_devolucion")
        fecha_real = self._valor(data, "fecha_devolucion_real")
        fecha_recepcion = self._valor(data, "fecha_recepcion")
        fecha_vencimiento = self._valor(data, "fecha_vencimiento")
        estado_documento = self._valor(data, "estado_documento")
        tipo_documento = self._valor(data, "tipo_documento")

        errores = {}

        # RN-19: si hay gestor asignado, se exige fecha de entrega y fecha
        # estimada de devolución (ambas, definidas al momento de asignar).
        if gestor:
            if not fecha_entrega_gestor:
                errores["fecha_entrega_gestor"] = (
                    "Al asignar un gestor externo, debe registrar la fecha de entrega."
                )
            if not fecha_estimada:
                errores["fecha_estimada_devolucion"] = (
                    "Al asignar un gestor externo, debe registrar la fecha estimada de devolución."
                )

        # Coherencia de fechas
        if fecha_entrega_gestor and fecha_estimada and fecha_estimada < fecha_entrega_gestor:
            errores["fecha_estimada_devolucion"] = (
                "No puede ser anterior a la fecha de entrega al gestor."
            )
        if fecha_entrega_gestor and fecha_real and fecha_real < fecha_entrega_gestor:
            errores["fecha_devolucion_real"] = (
                "No puede ser anterior a la fecha de entrega al gestor."
            )

        # Un documento 'recibido' o 'completado' debe tener fecha de recepción
        if estado_documento in ["recibido", "completado"] and not fecha_recepcion:
            errores["fecha_recepcion"] = (
                "Debe indicar la fecha de recepción cuando el estado es 'recibido' o 'completado'."
            )

        # Un documento 'completado' que vino de gestoría debe tener fecha real de devolución
        if estado_documento == "completado" and gestor and not fecha_real:
            errores["fecha_devolucion_real"] = (
                "Debe registrar la fecha real de devolución del gestor para marcar el documento como completado."
            )

        # RN-18 (vencimiento): si el tipo de documento requiere vencimiento
        # (VTV, Informe de Multas) y se marca como completado, debe cargarse
        # la fecha de vencimiento para poder alertar a tiempo.
        if tipo_documento and getattr(tipo_documento, "requiere_vencimiento", False):
            if estado_documento == "completado" and not fecha_vencimiento:
                errores["fecha_vencimiento"] = (
                    f"El tipo de documento '{tipo_documento.nombre}' requiere fecha de vencimiento."
                )

        if errores:
            raise serializers.ValidationError(errores)

        return data
