import React, { useState, useEffect } from 'react';

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

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({ nombre: '', direccion: '', ciudad: '', provincia: '', telefono: '', email: '', estado: 'activa' });
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
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5', zIndex: 1050 }}>
      <div className="modal-dialog modal-md modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">{initialData ? 'Editar Sucursal' : 'Nueva Sucursal'}</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label small fw-bold">Nombre de la Sucursal</label>
                  <input type="text" className="form-control" name="nombre" value={formData.nombre} onChange={handleChange} required />
                </div>
                <div className="col-12">
                  <label className="form-label small fw-bold">Dirección</label>
                  <input type="text" className="form-control" name="direccion" value={formData.direccion} onChange={handleChange} required />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Ciudad</label>
                  <input type="text" className="form-control" name="ciudad" value={formData.ciudad} onChange={handleChange} required />
                </div>
                <div className="col-md-6">
                  <label className="form-label small fw-bold">Provincia</label>
                  <input type="text" className="form-control" name="provincia" value={formData.provincia} onChange={handleChange} required />
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
                    <option value="activa">Activa</option>
                    <option value="inactiva">Inactiva</option>
                  </select>
                </div>
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold">Guardar Sucursal</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SucursalFormModal;
