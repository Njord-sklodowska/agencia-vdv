import React, { useState, useEffect } from 'react';

const ErrorMessage = ({ message }) => {
  if (!message) return null;
  return (
    <div className="invalid-feedback d-block" style={{ fontSize: '0.75rem', marginTop: '2px' }}>
      <i className="bi bi-exclamation-circle-fill me-1"></i>{message}
    </div>
  );
};

const ClienteFormModal = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    tipo_persona: 'fisica',
    dni_cuit: '',
    cuil: '',
    nombre: '',
    apellido: '',
    razon_social: '',
    nombre_fantasia: '',
    condicion_iva: '',
    telefono: '',
    telefono_alternativo: '',
    email: '',
    fecha_nacimiento: '',
    nacionalidad: '',
    domicilio_real: '',
    domicilio_fiscal: '',
    observaciones: '',
    estado: 'activo',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({
        tipo_persona: 'fisica',
        dni_cuit: '',
        cuil: '',
        nombre: '',
        apellido: '',
        razon_social: '',
        nombre_fantasia: '',
        condicion_iva: '',
        telefono: '',
        telefono_alternativo: '',
        email: '',
        fecha_nacimiento: '',
        nacionalidad: '',
        domicilio_real: '',
        domicilio_fiscal: '',
        observaciones: '',
        estado: 'activo',
      });
    }
    setErrors({});
  }, [initialData, isOpen]);

  const _limpiarNumeros = (valor) => {
    return valor.replace(/[-\s.]/g, '').replace(/[^\d]/g, '');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let valorLimpio = value;
    
    // Limpiar dni_cuit y cuil de guiones/caracteres especiales
    if (name === 'dni_cuit' || name === 'cuil') {
      valorLimpio = _limpiarNumeros(value);
    }
    
    setFormData(prev => ({ ...prev, [name]: valorLimpio }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrors({});
    
    try {
      await onSubmit(formData);
    } catch (error) {
      // Parsear errores del backend
      if (error.response && error.response.data) {
        setErrors(error.response.data);
      } else {
        setErrors({ non_field_errors: ['Error inesperado al guardar'] });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const getFieldError = (fieldName) => {
    return errors[fieldName] ? errors[fieldName].join(', ') : null;
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-person-fill me-2"></i>
              {initialData ? 'Editar Cliente' : 'Nuevo Cliente'}
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Tipo de Persona</label>
                  <select
                    className="form-select"
                    name="tipo_persona"
                    value={formData.tipo_persona}
                    onChange={handleChange}
                  >
                    <option value="fisica">Física</option>
                    <option value="juridica">Jurídica</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">
                    {formData.tipo_persona === 'fisica' ? 'DNI' : 'CUIT'}
                  </label>
                  <input
                    type="text"
                    className={`form-control ${getFieldError('dni_cuit') ? 'is-invalid' : ''}`}
                    name="dni_cuit"
                    value={formData.dni_cuit}
                    onChange={handleChange}
                    placeholder={formData.tipo_persona === 'fisica' ? 'Ej: 23123456' : 'Ej: 30232133545'}
                    maxLength={formData.tipo_persona === 'fisica' ? 8 : 11}
                    required
                  />
                  <small className="text-muted">
                    {formData.tipo_persona === 'fisica' ? '8 dígitos sin guiones' : '11 dígitos sin guiones'}
                  </small>
                  <ErrorMessage message={getFieldError('dni_cuit')} />
                </div>

                {formData.tipo_persona === 'fisica' ? (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nombre</label>
                      <input 
                        type="text" 
                        className={`form-control ${getFieldError('nombre') ? 'is-invalid' : ''}`}
                        name="nombre" 
                        value={formData.nombre} 
                        onChange={handleChange} 
                        required 
                      />
                      <ErrorMessage message={getFieldError('nombre')} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Apellido</label>
                      <input 
                        type="text" 
                        className={`form-control ${getFieldError('apellido') ? 'is-invalid' : ''}`}
                        name="apellido" 
                        value={formData.apellido} 
                        onChange={handleChange} 
                        required 
                      />
                      <ErrorMessage message={getFieldError('apellido')} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">CUIL</label>
                      <input 
                        type="text" 
                        className={`form-control ${getFieldError('cuil') ? 'is-invalid' : ''}`}
                        name="cuil" 
                        value={formData.cuil} 
                        onChange={handleChange} 
                        placeholder="Ej: 23231234565"
                        maxLength={11}
                        required 
                      />
                      <small className="text-muted">11 dígitos sin guiones</small>
                      <ErrorMessage message={getFieldError('cuil')} />
                    </div>
                  </>
                ) : (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Razón Social</label>
                      <input 
                        type="text" 
                        className={`form-control ${getFieldError('razon_social') ? 'is-invalid' : ''}`}
                        name="razon_social" 
                        value={formData.razon_social} 
                        onChange={handleChange} 
                        required 
                      />
                      <ErrorMessage message={getFieldError('razon_social')} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nombre Fantasía</label>
                      <input 
                        type="text" 
                        className={`form-control ${getFieldError('nombre_fantasia') ? 'is-invalid' : ''}`}
                        name="nombre_fantasia" 
                        value={formData.nombre_fantasia} 
                        onChange={handleChange} 
                      />
                      <ErrorMessage message={getFieldError('nombre_fantasia')} />
                    </div>
                  </>
                )}
	
<div className="col-md-6">
                  <label className="form-label small fw-bold">Condición IVA</label>
                  <select
                    className={`form-select ${getFieldError('condicion_iva') ? 'is-invalid' : ''}`}
                    name="condicion_iva"
                    value={formData.condicion_iva}
                    onChange={handleChange}
                  >
                    <option value="">Seleccione...</option>
                    <option value="responsable_inscripto">Responsable Inscripto</option>
                    <option value="monotributista">Monotributista</option>
                    <option value="exento">Exento</option>
                    <option value="consumidor_final">Consumidor Final</option>
                  </select>
                  <ErrorMessage message={getFieldError('condicion_iva')} />
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="bi bi-telephone"></i></span>
                    <input
                      type="text"
                      className={`form-control ${getFieldError('telefono') ? 'is-invalid' : ''}`}
                      name="telefono"
                      value={formData.telefono}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <ErrorMessage message={getFieldError('telefono')} />
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono Alternativo</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="bi bi-telephone-plus"></i></span>
                    <input
                      type="text"
                      className={`form-control ${getFieldError('telefono_alternativo') ? 'is-invalid' : ''}`}
                      name="telefono_alternativo"
                      value={formData.telefono_alternativo}
                      onChange={handleChange}
                    />
                  </div>
                  <ErrorMessage message={getFieldError('telefono_alternativo')} />
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
                  <ErrorMessage message={getFieldError('email')} />
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Estado</label>
                  <select
                    className={`form-select ${getFieldError('estado') ? 'is-invalid' : ''}`}
                    name="estado"
                    value={formData.estado}
                    onChange={handleChange}
                  >
                    <option value="activo">Activo</option>
                    <option value="inactivo">Inactivo</option>
                  </select>
                  <ErrorMessage message={getFieldError('estado')} />
                </div>

                {formData.tipo_persona === 'fisica' && (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Fecha de Nacimiento</label>
                      <input
                        type="date"
                        className={`form-control ${getFieldError('fecha_nacimiento') ? 'is-invalid' : ''}`}
                        name="fecha_nacimiento"
                        value={formData.fecha_nacimiento}
                        onChange={handleChange}
                      />
                      <ErrorMessage message={getFieldError('fecha_nacimiento')} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nacionalidad</label>
                      <input
                        type="text"
                        className={`form-control ${getFieldError('nacionalidad') ? 'is-invalid' : ''}`}
                        name="nacionalidad"
                        value={formData.nacionalidad}
                        onChange={handleChange}
                      />
                      <ErrorMessage message={getFieldError('nacionalidad')} />
                    </div>
                  </>
                )}

                <div className="col-12">
                  <label className="form-label small fw-bold">Domicilio Real</label>
                  <input
                    type="text"
                    className={`form-control ${getFieldError('domicilio_real') ? 'is-invalid' : ''}`}
                    name="domicilio_real"
                    value={formData.domicilio_real}
                    onChange={handleChange}
                    required
                  />
                  <ErrorMessage message={getFieldError('domicilio_real')} />
                </div>

                <div className="col-12">
                  <label className="form-label small fw-bold">Domicilio Fiscal</label>
                  <input
                    type="text"
                    className={`form-control ${getFieldError('domicilio_fiscal') ? 'is-invalid' : ''}`}
                    name="domicilio_fiscal"
                    value={formData.domicilio_fiscal}
                    onChange={handleChange}
                  />
                  <ErrorMessage message={getFieldError('domicilio_fiscal')} />
                </div>

                <div className="col-12">
                  <label className="form-label small fw-bold">Observaciones</label>
                  <textarea
                    className={`form-control ${getFieldError('observaciones') ? 'is-invalid' : ''}`}
                    name="observaciones"
                    rows="3"
                    value={formData.observaciones}
                    onChange={handleChange}
                  ></textarea>
                  <ErrorMessage message={getFieldError('observaciones')} />
                </div>
              </div>
            </div>
            {errors.non_field_errors && (
              <div className="mx-3 mb-3">
                <div className="alert alert-danger py-2 mb-0" style={{ fontSize: '0.875rem' }}>
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  {errors.non_field_errors.join(', ')}
                </div>
              </div>
            )}
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold" disabled={isSubmitting}>
                {isSubmitting ? 'Guardando...' : 'Guardar Cliente'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ClienteFormModal;
