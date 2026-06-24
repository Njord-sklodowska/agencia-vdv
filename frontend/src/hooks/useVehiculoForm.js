import { useState, useEffect } from 'react';
import { inventarioApi } from '../api/inventarioApi';

export const useVehiculoForm = (vehicleToEdit = null) => {
  const initialFormState = {
    marca: '',
    modelo: '',
    anio: '',
    precio: '',
    patente: '',
    estado: 'Nuevo',
    descripcion: '',
    kilometraje: '',
  };

  const [formData, setFormData] = useState(initialFormState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [validations, setValidations] = useState({});

  useEffect(() => {
    if (vehicleToEdit) {
      setFormData({
        marca: vehicleToEdit.marca_nombre || vehicleToEdit.marca || '',
        modelo: vehicleToEdit.modelo_nombre || vehicleToEdit.modelo || '',
        anio: vehicleToEdit.anio || '',
        precio: vehicleToEdit.precio || '',
        patente: vehicleToEdit.patente || '',
        estado: vehicleToEdit.estado || 'Nuevo',
        descripcion: vehicleToEdit.descripcion || '',
        kilometraje: vehicleToEdit.kilometraje || '',
      });
    } else {
      setFormData(initialFormState);
    }
  }, [vehicleToEdit]);

  const validateField = (name, value) => {
    let error = '';
    if (name === 'patente') {
      // Validación simple de patente (ej. ABC 123 o ABC123)
      const patenteRegex = /^[A-Z]{3}\s?\d{3}[A-Z]?$/i;
      if (!patenteRegex.test(value)) {
        error = 'Formato de patente inválido (Ej: ABC 123)';
      }
    }
    if (name === 'anio') {
      const currentYear = new Date().getFullYear();
      if (value < 1900 || value > currentYear + 1) {
        error = `Año inválido (1900 - ${currentYear + 1})`;
      }
    }
    return error;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Validar en tiempo real
    const fieldError = validateField(name, value);
    setValidations(prev => ({ ...prev, [name]: fieldError }));
  };

  const handleSubmit = async (asyncCallback) => {
    // Validación final antes de enviar
    const errors = {};
    Object.keys(formData).forEach(key => {
      const err = validateField(key, formData[key]);
      if (err) errors[key] = err;
    });

    if (Object.keys(errors).length > 0) {
      setValidations(errors);
      setError('Por favor, corrija los errores en el formulario.');
      return { success: false };
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      if (vehicleToEdit) {
        await inventarioApi.updateVehiculo(vehicleToEdit.id, formData);
      } else {
        await inventarioApi.createVehiculo(formData);
      }
      setSuccess(true);
      return { success: true };
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Hubo un error al procesar la solicitud.';
      setError(errMsg);
      return { success: false, error: errMsg };
    } finally {
      setLoading(false);
    }
  };

  return {
    formData,
    setFormData,
    handleChange,
    handleSubmit,
    loading,
    error,
    success,
    setSuccess,
    validations,
    setError,
  };
};
