import React from 'react';

/**
 * Componente reutilizable para mostrar errores de validación debajo de campos.
 * 
 * Uso:
 * <FormError message={error} />
 * 
 * @param {string} message - Mensaje de error a mostrar
 */
const FormError = ({ message }) => {
  if (!message) return null;
  
  return (
    <div 
      className="invalid-feedback d-block" 
      style={{ 
        fontSize: '0.75rem', 
        marginTop: '2px',
        color: '#dc3545'
      }}
    >
      <i className="bi bi-exclamation-circle-fill me-1"></i>
      {message}
    </div>
  );
};

export default FormError;
