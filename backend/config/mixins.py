from auditoria.models import LogAuditoria

class AuditMixin:
    """
    Mixin para registrar automáticamente acciones de creación, 
    modificación y eliminación en el Log de Auditoría.
    """
    # Cada ViewSet que use este Mixin deberá definir su nombre de módulo
    # Ejemplo: modulo_name = "Inventario"
    modulo_name = "Sistema"

    def _get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def _log_action(self, instance, action, description):
        LogAuditoria.objects.create(
            usuario=self.request.user,
            accion=action,
            modulo=self.modulo_name,
            tabla_afectada=instance._meta.model_name,
            registro_id=instance.pk,
            descripcion=description,
            ip=self._get_client_ip()
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        desc = f"Se creó el registro {instance._meta.verbose_name} con ID: {instance.pk}"
        self._log_action(instance, 'CREAR', desc)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        desc = f"Se modificó el registro {instance._meta.verbose_name} con ID: {instance.pk}"
        self._log_action(instance, 'MODIFICAR', desc)
        return instance

    def perform_destroy(self, instance):
        desc = f"Se eliminó el registro {instance._meta.verbose_name} con ID: {instance.pk}"
        self._log_action(instance, 'ELIMINAR', desc)
        instance.delete()
