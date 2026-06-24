import React, { useState, useEffect } from 'react';

const TallerFormModal = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    direccion: '',
    telefono: '',
    email: '',
    estado: 'activo',
  });

  useEffect(() => {
    if (isOpen) {
      if (initialData) {
        setFormData(initialData);
      } else {
        setFormData({ nombre: '', direccion: '', telefono: '', email: '', estado: 'activo' });
      }
    }
  }, [initialData, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-md modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">{initialData ? 'Editar Taller' : 'Nuevo Taller'}</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label small fw-bold">Nombre del Taller</label>
                  <input type="text" className="form-control" name="nombre" value={formData.nombre} onChange={handleChange} required />
                </div>
                <div className="col-12">
                  <label className="form-label small fw-bold">Dirección</label>
                  <input type="text" className="form-control" name="direccion" value={formData.direccion} onChange={handleChange} />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Teléfono</label>
                  <input type="text" className="form-control" name="telefono" value={formData.telefono} onChange={handleChange} />
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
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold">Guardar Taller</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TallerFormModal;
