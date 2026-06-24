import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { inventarioApi } from '../../api/inventarioApi';

const NuevoVehiculoPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState({
    marca: '',
    modelo: '',
    año: '',
    precio: '',
    patente: '',
    estado: 'Nuevo',
    descripcion: '',
    kilometraje: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await inventarioApi.createVehiculo(formData);
      setSuccess(true);
      setTimeout(() => {
        navigate('/inventario');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Hubo un error al guardar el vehículo. Inténtalo de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fade-in">
      <div className="page-header">
        <div>
          <h4 className="page-title">Alta de Vehículo</h4>
          <p className="page-subtitle">Ingrese los detalles de la unidad para añadirla al stock.</p>
        </div>
        <button className="btn btn-outline-secondary btn-sm" onClick={() => navigate('/inventario')}>
          <i className="bi bi-arrow-left me-1"></i> Volver al Stock
        </button>
      </div>

      <div className="accent-bar mb-4"></div>

      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card form-card">
            <div className="card-header">
              <h6 className="form-section-title mb-0">
                <i className="bi bi-car-front-fill me-2 text-primary"></i> Información General
              </h6>
            </div>

            <div className="card-body p-4">
              {success && (
                <div className="alert alert-success d-flex align-items-center" role="alert">
                  <i className="bi bi-check-circle-fill me-2"></i>
                  <div>¡Vehículo guardado exitosamente! Redirigiendo al stock...</div>
                </div>
              )}

              {error && (
                <div className="alert alert-danger d-flex align-items-center" role="alert">
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  <div>{error}</div>
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row g-4">
                  <div className="col-md-6">
                    <label className="form-label form-label-custom">Marca</label>
                    <input type="text" name="marca" className="form-control" placeholder="Ej: Toyota" value={formData.marca} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label form-label-custom">Modelo</label>
                    <input type="text" name="modelo" className="form-control" placeholder="Ej: Hilux" value={formData.modelo} onChange={handleChange} required />
                  </div>

                  <div className="col-md-4">
                    <label className="form-label form-label-custom">Año</label>
                    <input type="number" name="año" className="form-control" placeholder="2024" value={formData.año} onChange={handleChange} required />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label form-label-custom">Precio</label>
                    <div className="input-group">
                      <span className="input-group-text bg-light border-end-0">$</span>
                      <input type="text" name="precio" className="form-control border-start-0" placeholder="0.00" value={formData.precio} onChange={handleChange} required />
                    </div>
                  </div>
                  <div className="col-md-4">
                    <label className="form-label form-label-custom">Estado</label>
                    <select name="estado" className="form-select" value={formData.estado} onChange={handleChange}>
                      <option value="Nuevo">Nuevo</option>
                      <option value="Usado">Usado</option>
                    </select>
                  </div>

                  <div className="col-md-6">
                    <label className="form-label form-label-custom">Patente / VIN</label>
                    <input type="text" name="patente" className="form-control" placeholder="Ingrese la patente" value={formData.patente} onChange={handleChange} required />
                  </div>

                  <div className="col-md-6">
                    <label className="form-label form-label-custom">Kilometraje</label>
                    <input
                      type="number"
                      name="kilometraje"
                      className="form-control"
                      placeholder="0 km"
                      value={formData.kilometraje}
                      onChange={handleChange}
                      disabled={formData.estado === 'Nuevo'}
                      className={formData.estado === 'Nuevo' ? 'form-control-disabled' : ''}
                    />
                  </div>

                  <div className="col-12">
                    <label className="form-label form-label-custom">Notas / Descripción</label>
                    <textarea name="descripcion" className="form-control" rows="3" placeholder="Detalles adicionales del vehículo..." value={formData.descripcion} onChange={handleChange}></textarea>
                  </div>
                </div>

                <div className="mt-5 d-flex gap-3 justify-content-end">
                  <button type="button" className="btn btn-outline-secondary px-4" onClick={() => navigate('/inventario')}>
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn-gold" disabled={loading}>
                    {loading ? (
                      <><span className="spinner-border spinner-border-sm me-2"></span>Guardando...</>
                    ) : (
                      <><i className="bi bi-save me-1"></i> Guardar Vehículo</>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NuevoVehiculoPage;
