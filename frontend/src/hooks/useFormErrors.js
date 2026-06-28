import { useState, useCallback } from 'react';

/**
 * Hook para manejar errores de validación del backend en formularios.
 * 
 * Uso:
 * const { errors, getFieldError, handleSubmit, setErrors, clearErrors } = useFormErrors();
 * 
 * // En el submit:
 * const success = await handleSubmit(async () => {
 *   await miApi.guardar(datos);
 * });
 * 
 * // En el campo:
 * <FormError message={getFieldError('nombre')} />
 * 
 * @returns {object} - { errors, getFieldError, handleSubmit, setErrors, clearErrors }
 */
const useFormErrors = () => {
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  /**
   * Obtiene el mensaje de error para un campo específico.
   * @param {string} fieldName - Nombre del campo
   * @returns {string|null} - Mensaje de error o null
   */
  const getFieldError = useCallback((fieldName) => {
    if (errors[fieldName]) {
      return Array.isArray(errors[fieldName]) 
        ? errors[fieldName].join(', ') 
        : errors[fieldName];
    }
    return null;
  }, [errors]);

  /**
   * Ejecuta una función de submit y captura errores del backend.
   * @param {Function} submitFn - Función async que realiza el guardado
   * @returns {Promise<boolean>} - true si fue exitoso, false si hubo error
   */
  const handleSubmit = useCallback(async (submitFn) => {
    setIsSubmitting(true);
    setErrors({});

    try {
      await submitFn();
      return true;
    } catch (error) {
      console.error('Error en formulario:', error);
      
      if (error.response?.data) {
        // Error de validación del backend (400)
        setErrors(error.response.data);
      } else if (error.response) {
        // Otro error HTTP (500, etc.)
        setErrors({ 
          non_field_errors: [`Error del servidor (${error.response.status})`] 
        });
      } else if (error.request) {
        // Error de red
        setErrors({ non_field_errors: ['Error de conexión con el servidor'] });
      } else {
        // Error inesperado
        setErrors({ non_field_errors: ['Error inesperado al procesar la solicitud'] });
      }
      
      return false;
    } finally {
      setIsSubmitting(false);
    }
  }, []);

  /**
   * Limpia todos los errores.
   */
  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  /**
   * Establece un error manualmente para un campo.
   * @param {string} fieldName - Nombre del campo
   * @param {string} message - Mensaje de error
   */
  const setFieldError = useCallback((fieldName, message) => {
    setErrors(prev => ({
      ...prev,
      [fieldName]: [message]
    }));
  }, []);

  return {
    errors,
    getFieldError,
    handleSubmit,
    setErrors,
    clearErrors,
    setFieldError,
    isSubmitting
  };
};

export default useFormErrors;
