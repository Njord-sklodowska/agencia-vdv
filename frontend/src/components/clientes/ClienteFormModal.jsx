import React, { useState, useEffect } from 'react';

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

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
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
                    className="form-control"
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
                </div>

                {formData.tipo_persona === 'fisica' ? (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nombre</label>
                      <input type="text" className="form-control" name="nombre" value={formData.nombre} onChange={handleChange} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Apellido</label>
                      <input type="text" className="form-control" name="apellido" value={formData.apellido} onChange={handleChange} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">CUIL</label>
                      <input 
                        type="text" 
                        className="form-control" 
                        name="cuil" 
                        value={formData.cuil} 
                        onChange={handleChange} 
                        placeholder="Ej: 23231234565"
                        maxLength={11}
                        required 
                      />
                      <small className="text-muted">11 dígitos sin guiones</small>
                    </div>
                  </>
                ) : (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Razón Social</label>
                      <input type="text" className="form-control" name="razon_social" value={formData.razon_social} onChange={handleChange} required />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nombre Fantasía</label>
                      <input type="text" className="form-control" name="nombre_fantasia" value={formData.nombre_fantasia} onChange={handleChange} />
                    </div>
                  </>
                )}
	
		<div className="col-md-6">
                  <label className="form-label small fw-bold">Condición IVA</label>
                  <select
                    className="form-select"
                    name="condicion_iva"
                    value={formData.condicion_iva}
                    onChange={handleChange}
                  >
                    <option value="responsable_inscripto">Responsable_inscripto</option>
                    <option value="monotributista">Monotributista</option>
                    <option value="exento">Exento</option>
                    <option value="consumidor_final">Consumidor_final</option>
                  </select>
                </div>                

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="bi bi-telephone"></i></span>
                    <input type="text" className="form-control" name="telefono" value={formData.telefono} onChange={handleChange} required />
                  </div>
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono Alternativo</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="bi bi-telephone-plus"></i></span>
                    <input type="text" className="form-control" name="telefono_alternativo" value={formData.telefono_alternativo} onChange={handleChange} />
                  </div>
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Email</label>
                  <input type="email" className="form-control" name="email" value={formData.email} onChange={handleChange} />
                </div>

                <div className="col-md-6">
                  <label className="form-label small fw-bold">Estado</label>
                  <select className="form-select" name="estado" value={formData.estado} onChange={handleChange}>
                    <option value="activo">Activo</option>
                    <option value="inactivo">Inactivo</option>
                  </select>
                </div>

                {formData.tipo_persona === 'fisica' && (
                  <>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Fecha de Nacimiento</label>
                      <input type="date" className="form-control" name="fecha_nacimiento" value={formData.fecha_nacimiento} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-bold">Nacionalidad</label>
                      <input type="text" className="form-control" name="nacionalidad" value={formData.nacionalidad} onChange={handleChange} />
                    </div>
                  </>
                )}

                <div className="col-12">
                  <label className="form-label small fw-bold">Domicilio Real</label>
                  <input type="text" className="form-control" name="domicilio_real" value={formData.domicilio_real} onChange={handleChange} required />
                </div>

                <div className="col-12">
                  <label className="form-label small fw-bold">Domicilio Fiscal</label>
                  <input type="text" className="form-control" name="domicilio_fiscal" value={formData.domicilio_fiscal} onChange={handleChange} />
                </div>

                <div className="col-12">
                  <label className="form-label small fw-bold">Observaciones</label>
                  <textarea className="form-control" name="observaciones" rows="3" value={formData.observaciones} onChange={handleChange}></textarea>
                </div>
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold">
                Guardar Cliente
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ClienteFormModal;
