import React, { useState, useEffect } from 'react';
import FormError from '../common/FormError';
import useFormErrors from '../../hooks/useFormErrors';

const SucursalFormModal = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
    ciudad: '',
    provincia: '',
    telefono: '',
    email: '',
    estado: 'activa',
  });

  const { errors, getFieldError, handleSubmit, clearErrors, isSubmitting } = useFormErrors();

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({ nombre: '', direccion: '', ciudad: '', provincia: '', telefono: '', email: '', estado: 'activa' });
    }
    clearErrors();
  }, [initialData, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const onFormSubmit = async (e) => {
    e.preventDefault();
    
    await handleSubmit(async () => {
      await onSubmit(formData);
      onClose();
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-md modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">
              <i className={`bi ${initialData ? 'bi-pencil-square' : 'bi-building-add'} me-2`}></i>
              {initialData ? 'Editar Sucursal' : 'Nueva Sucursal'}
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={onFormSubmit}>
            <div className="modal-body modal-body-light">
              {errors.non_field_errors && (
                <div className="alert alert-danger py-2 mb-3" style={{ fontSize: '0.875rem' }}>
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  {errors.non_field_errors.join(', ')}
                </div>
              )}
              
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label small fw-bold">Nombre de la Sucursal</label>
                  <input 
                    type="text" 
                    className={`form-control ${getFieldError('nombre') ? 'is-invalid' : ''}`}
                    name="nombre" 
                    value={formData.nombre} 
                    onChange={handleChange} 
                    required 
                  />
                  <FormError message={getFieldError('nombre')} />
                </div>
                <div className="col-12">
                  <label className="form-label small fw-bold">Dirección</label>
                  <input 
                    type="text" 
                    className={`form-control ${getFieldError('direccion') ? 'is-invalid' : ''}`}
                    name="direccion" 
                    value={formData.direccion} 
                    onChange={handleChange} 
                    required 
                  />
                  <FormError message={getFieldError('direccion')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Ciudad</label>
                  <input 
                    type="text" 
                    className={`form-control ${getFieldError('ciudad') ? 'is-invalid' : ''}`}
                    name="ciudad" 
                    value={formData.ciudad} 
                    onChange={handleChange} 
                    required 
                  />
                  <FormError message={getFieldError('ciudad')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Provincia</label>
                  <input 
                    type="text" 
                    className={`form-control ${getFieldError('provincia') ? 'is-invalid' : ''}`}
                    name="provincia" 
                    value={formData.provincia} 
                    onChange={handleChange} 
                    required 
                  />
                  <FormError message={getFieldError('provincia')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono</label>
                  <input 
                    type="text" 
                    className={`form-control ${getFieldError('telefono') ? 'is-invalid' : ''}`}
                    name="telefono" 
                    value={formData.telefono} 
                    onChange={handleChange} 
                  />
                  <FormError message={getFieldError('telefono')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Email</label>
                  <input 
                    type="email" 
                    className={`form-control ${getFieldError('email') ? 'is-invalid' : ''}`}
                    name="email" 
                    value={formData.email} 
                    onChange={handleChange} 
                  />
                  <FormError message={getFieldError('email')} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Estado</label>
                  <select 
                    className={`form-select ${getFieldError('estado') ? 'is-invalid' : ''}`}
                    name="estado" 
                    value={formData.estado} 
                    onChange={handleChange}
                  >
                    <option value="activa">Activa</option>
                    <option value="inactiva">Inactiva</option>
                  </select>
                  <FormError message={getFieldError('estado')} />
                </div>
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold" disabled={isSubmitting}>
                {isSubmitting ? (
                  <><span className="spinner-border spinner-border-sm me-2"></span>Guardando...</>
                ) : (
                  'Guardar Sucursal'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SucursalFormModal;
