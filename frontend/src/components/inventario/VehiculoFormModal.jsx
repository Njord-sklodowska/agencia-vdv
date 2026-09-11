import React, { useState } from 'react';
import { useVehiculoForm } from '../../hooks/useVehiculoForm';
import VehiculoFotos from './VehiculoFotos';

const VehiculoFormModal = ({ isOpen, onClose, onSave, vehicleToEdit }) => {
  const [activeTab, setActiveTab] = useState('datos');
  const {
    formData,
    handleChange,
    handleSubmit,
    loading,
    error,
    success,
    setSuccess,
    validations,
    setError,
  } = useVehiculoForm(vehicleToEdit);

  if (!isOpen) return null;

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const result = await handleSubmit();
    if (result.success) {
      setTimeout(() => {
        setSuccess(false);
        onClose();
        onSave();
      }, 1500);
    }
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(4px)', zIndex: 1050 }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content modal-form-content">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-car-front-fill me-2"></i>
              {vehicleToEdit ? 'Editar Vehículo' : 'Nuevo Vehículo'}
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>

          <div className="d-flex bg-light border-bottom">
            <button
              className={`btn py-2 px-4 modal-tab-btn ${activeTab === 'datos' ? 'modal-tab-active' : 'text-muted'}`}
              onClick={() => setActiveTab('datos')}
            >
              📋 Datos Generales
            </button>
            <button
              className={`btn py-2 px-4 modal-tab-btn ${activeTab === 'fotos' ? 'modal-tab-active' : 'text-muted'}`}
              onClick={() => setActiveTab('fotos')}
            >
              📸 Fotografías
            </button>
          </div>

          <div className="modal-body p-4">
            {success && (
              <div className="alert alert-success d-flex align-items-center mb-4 shadow-sm" role="alert">
                <i className="bi bi-check-circle-fill me-2"></i>
                <div>¡Vehículo guardado exitosamente!</div>
              </div>
            )}

            {error && (
              <div className="alert alert-danger d-flex align-items-center mb-4 shadow-sm" role="alert">
                <i className="bi bi-exclamation-triangle-fill me-2"></i>
                <div>{error}</div>
              </div>
            )}

            {activeTab === 'datos' ? (
              <form onSubmit={handleFormSubmit} id="vehiculo-form">
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Marca</label>
                    <input type="text" name="marca" className="form-control" placeholder="Ej: Toyota" value={formData.marca} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Modelo</label>
                    <input type="text" name="modelo" className="form-control" placeholder="Ej: Hilux" value={formData.modelo} onChange={handleChange} required />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Año</label>
                    <input
                      type="number" name="anio" className={`form-control ${validations.anio ? 'is-invalid' : ''}`}
                      placeholder="2024" value={formData.anio} onChange={handleChange} required
                    />
                    {validations.anio && <div className="invalid-feedback d-block">{validations.anio}</div>}
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Precio</label>
                    <div className="input-group">
                      <span className="input-group-text bg-light border-end-0">$</span>
                      <input type="text" name="precio" className="form-control border-start-0" placeholder="0.00" value={formData.precio} onChange={handleChange} required />
                    </div>
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Estado</label>
                    <select name="estado" className="form-select" value={formData.estado} onChange={handleChange}>
                      <option value="Nuevo">Nuevo</option>
                      <option value="Usado">Usado</option>
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Patente / VIN</label>
                    <input
                      type="text" name="patente" className={`form-control ${validations.patente ? 'is-invalid' : ''}`}
                      placeholder="Ej: ABC 123" value={formData.patente} onChange={handleChange} required
                    />
                    {validations.patente && <div className="invalid-feedback d-block">{validations.patente}</div>}
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Kilometraje</label>
                    <input
                      type="number" name="kilometraje" className="form-control"
                      placeholder="0 km" value={formData.kilometraje} onChange={handleChange}
                      disabled={formData.estado === 'Nuevo'}
                    />
                  </div>
                  <div className="col-12">
                    <label className="form-label small fw-bold">Notas / Descripción</label>
                    <textarea name="descripcion" className="form-control" rows="3" placeholder="Detalles adicionales..." value={formData.descripcion} onChange={handleChange}></textarea>
                  </div>
                </div>
              </form>
            ) : (
              <div className="py-2">
                <VehiculoFotos vehiculoId={vehicleToEdit?.id} onRefresh={onSave} />
              </div>
            )}
          </div>

          <div className="modal-footer modal-footer-light">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
            {activeTab === 'datos' && (
              <button type="submit" form="vehiculo-form" className="btn btn-gold" disabled={loading}>
                {loading ? (
                  <><span className="spinner-border spinner-border-sm me-2"></span>Guardando...</>
                ) : (
                  <><i className="bi bi-save me-1"></i> {vehicleToEdit ? 'Actualizar Vehículo' : 'Guardar Vehículo'}</>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehiculoFormModal;
