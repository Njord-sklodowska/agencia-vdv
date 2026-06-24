import React, { useState, useEffect } from 'react';

const ParametroFormModal = ({ isOpen, onClose, onSave, parametroToEdit }) => {
  const [formData, setFormData] = useState({
    nombre_parametro: '',
    valor: '',
    tipo_dato: 'texto',
    descripcion: '',
  });

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
  }, [parametroToEdit, isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
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
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              <div className="row g-3">
                <div className="col-12">
                  <label className="form-label fw-medium">Nombre del Parámetro</label>
                  <input
                    type="text"
                    name="nombre_parametro"
                    className="form-control"
                    value={formData.nombre_parametro}
                    onChange={handleChange}
                    disabled={!!parametroToEdit}
                    required
                    placeholder="Ej: LIMITE_USUARIOS_SISTEMA"
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label fw-medium">Valor</label>
                  <input
                    type="text"
                    name="valor"
                    className="form-control"
                    value={formData.valor}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="col-md-6">
                  <label className="form-label fw-medium">Tipo de Dato</label>
                  <select
                    name="tipo_dato"
                    className="form-select"
                    value={formData.tipo_dato}
                    onChange={handleChange}
                  >
                    <option value="texto">Texto</option>
                    <option value="numero">Número</option>
                    <option value="booleano">Booleano</option>
                    <option value="fecha">Fecha</option>
                  </select>
                </div>
                <div className="col-12">
                  <label className="form-label fw-medium">Descripción</label>
                  <textarea
                    name="descripcion"
                    className="form-control"
                    rows="3"
                    value={formData.descripcion}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold">
                Guardar Cambios
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ParametroFormModal;
