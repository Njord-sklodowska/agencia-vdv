import React, { useState, useEffect } from 'react';
import FormError from '../common/FormError';
import useFormErrors from '../../hooks/useFormErrors';

const ParametroFormModal = ({ isOpen, onClose, onSave, parametroToEdit }) => {
  const [formData, setFormData] = useState({
    nombre_parametro: '',
    valor: '',
    tipo_dato: 'texto',
    descripcion: '',
  });

  const { errors, getFieldError, handleSubmit, clearErrors, isSubmitting } = useFormErrors();

  useEffect(() => {
    if (parametroToEdit) {
      setFormData({
        nombre_parametro: parametroToEdit.nombre_parametro || '',
        valor: parametroToEdit.valor || '',
        tipo_dato: parametroToEdit.tipo_dato || 'texto',
        descripcion: parametroToEdit.descripcion || '',
      });
    } else {
      setFormData({
        nombre_parametro: '',
        valor: '',
        tipo_dato: 'texto',
        descripcion: '',
      });
    }
    clearErrors();
  }, [parametroToEdit, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    
    await handleSubmit(async () => {
      await onSave(formData);
      onClose();
    });
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-md">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-gear-fill me-2"></i>
              {parametroToEdit ? 'Editar Parámetro' : 'Nuevo Parámetro'}
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleFormSubmit}>
            <div className="modal-body modal-body-light">
              {errors.non_field_errors && (
                <div className="alert alert-danger py-2 mb-3" style={{ fontSize: '0.875rem' }}>
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  {errors.non_field_errors.join(', ')}
                </div>
              )}
              
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label fw-medium">Nombre del Parámetro</label>
                  <input
                    type="text"
                    name="nombre_parametro"
                    className={`form-control ${getFieldError('nombre_parametro') ? 'is-invalid' : ''}`}
                    value={formData.nombre_parametro}
                    onChange={handleChange}
                    disabled={!!parametroToEdit}
                    required
                    placeholder="Ej: LIMITE_USUARIOS_SISTEMA"
                  />
                  <FormError message={getFieldError('nombre_parametro')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label fw-medium">Valor</label>
                  <input
                    type="text"
                    name="valor"
                    className={`form-control ${getFieldError('valor') ? 'is-invalid' : ''}`}
                    value={formData.valor}
                    onChange={handleChange}
                    required
                  />
                  <FormError message={getFieldError('valor')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label fw-medium">Tipo de Dato</label>
                  <select
                    name="tipo_dato"
                    className={`form-select ${getFieldError('tipo_dato') ? 'is-invalid' : ''}`}
                    value={formData.tipo_dato}
                    onChange={handleChange}
                  >
                    <option value="texto">Texto</option>
                    <option value="numero">Número</option>
                    <option value="booleano">Booleano</option>
                    <option value="fecha">Fecha</option>
                  </select>
                  <FormError message={getFieldError('tipo_dato')} />
                </div>
                <div className="col-12">
                  <label className="form-label fw-medium">Descripción</label>
                  <textarea
                    name="descripcion"
                    className={`form-control ${getFieldError('descripcion') ? 'is-invalid' : ''}`}
                    rows="3"
                    value={formData.descripcion}
                    onChange={handleChange}
                  />
                  <FormError message={getFieldError('descripcion')} />
                </div>
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold" disabled={isSubmitting}>
                {isSubmitting ? (
                  <><span className="spinner-border spinner-border-sm me-2"></span>Guardando...</>
                ) : (
                  'Guardar Cambios'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ParametroFormModal;
