import React, { useState, useEffect } from 'react';
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
      {/* Header Section */}
      <div className="d-flex justify-content-between align-items-center mb-2">
        <div>
          <h4 className="mb-0 fw-bold" style={{ color: 'var(--text-dark)' }}>Alta de Vehículo</h4>
          <p className="mb-0 text-muted small">Ingrese los detalles de la unidad para añadirla al stock.</p>
        </div>
        <button 
          className="btn btn-outline-custom btn-sm" 
          onClick={() => navigate('/inventario')}
        >
          <i className="bi bi-arrow-left me-1"></i> Volver al Stock
        </button>
      </div>
      
      <div className="accent-bar mb-4"></div>

      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-sm border-0" style={{ borderRadius: '16px', background: '#fff', overflow: 'hidden' }}>
            <div className="card-header bg-white py-3 border-bottom" style={{ borderBottom: '1px solid #e8dfe1' }}>
              <h6 className="mb-0 fw-bold" style={{ color: 'var(--text-dark)' }}>
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
                  {/* Marca y Modelo */}
                  <div className="col-md-6">
                    <label className="form-label small fw-medium text-muted">Marca</label>
                    <input 
                      type="text" 
                      name="marca" 
                      className="form-control" 
                      placeholder="Ej: Toyota" 
                      value={formData.marca}
                      onChange={handleChange}
                      required
                      style={{ border: '1px solid #e8dfe1' }}
                    />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-medium text-muted">Modelo</label>
                    <input 
                      type="text" 
                      name="modelo" 
                      className="form-control" 
                      placeholder="Ej: Hilux" 
                      value={formData.modelo}
                      onChange={handleChange}
                      required
                      style={{ border: '1px solid #e8dfe1' }}
                    />
                  </div>

                  {/* Año y Precio */}
                  <div className="col-md-4">
                    <label className="form-label small fw-medium text-muted">Año</label>
                    <input 
                      type="number" 
                      name="año" 
                      className="form-control" 
                      placeholder="2024" 
                      value={formData.año}
                      onChange={handleChange}
                      required
                      style={{ border: '1px solid #e8dfe1' }}
                    />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-medium text-muted">Precio</label>
                    <div className="input-group">
                      <span className="input-group-text bg-light border-end-0" style={{ border: '1px solid #e8dfe1' }}>$</span>
                      <input 
                        type="text" 
                        name="precio" 
                        className="form-control border-start-0" 
                        placeholder="0.00" 
                        value={formData.precio}
                        onChange={handleChange}
                        required
                        style={{ border: '1px solid #e8dfe1' }}
                      />
                    </div>
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-medium text-muted">Estado</label>
                    <select 
                      name="estado" 
                      className="form-select" 
                      value={formData.estado}
                      onChange={handleChange}
                      style={{ border: '1px solid #e8dfe1' }}
                    >
                      <option value="Nuevo">Nuevo</option>
                      <option value="Usado">Usado</option>
                    </select>
                  </div>

                  {/* Patente / VIN */}
                  <div className="col-md-6">
                    <label className="form-label small fw-medium text-muted">Patente / VIN</label>
                    <input 
                      type="text" 
                      name="patente" 
                      className="form-control" 
                      placeholder="Ingrese la patente" 
                      value={formData.patente}
                      onChange={handleChange}
                      required
                      style={{ border: '1px solid #e8dfe1' }}
                    />
                  </div>

                  {/* Kilometraje (Solo si es usado) */}
                  <div className="col-md-6">
                    <label className="form-label small fw-medium text-muted">Kilometraje</label>
                    <input 
                      type="number" 
                      name="kilometraje" 
                      className="form-control" 
                      placeholder="0 km" 
                      value={formData.kilometraje}
                      onChange={handleChange}
                      disabled={formData.estado === 'Nuevo'}
                      style={{ 
                        border: '1px solid #e8dfe1',
                        backgroundColor: formData.estado === 'Nuevo' ? '#f8f9fa' : '#fff'
                      }}
                    />
                  </div>

                  {/* Descripción */}
                  <div className="col-12">
                    <label className="form-label small fw-medium text-muted">Notas / Descripción</label>
                    <textarea 
                      name="descripcion" 
                      className="form-control" 
                      rows="3" 
                      placeholder="Detalles adicionales del vehículo..." 
                      value={formData.descripcion}
                      onChange={handleChange}
                      style={{ border: '1px solid #e8dfe1' }}
                    ></textarea>
                  </div>
                </div>

                <div className="mt-5 d-flex gap-3 justify-content-end">
                  <button 
                    type="button" 
                    className="btn btn-outline-custom px-4" 
                    onClick={() => navigate('/inventario')}
                  >
                    Cancelar
                  </button>
                  <button 
                    type="submit" 
                    className="btn btn-gold px-5 py-2" 
                    disabled={loading}
                  >
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

      <style>{`
        .fade-in {
          animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .btn-gold {
          background: var(--accent-gold);
          color: var(--primary-dark);
          border: none;
          font-weight: 600;
          font-size: 14px;
          transition: all 0.2s;
        }
        .btn-gold:hover { background: #b89c45; color: var(--primary-dark); }
        .btn-outline-custom {
          border: 1px solid #d4c0c4;
          color: #5a4a4e;
          background: transparent;
          font-size: 13px;
          transition: all 0.2s;
        }
        .btn-outline-custom:hover {
          background: #f5f0f1;
          border-color: var(--accent-gold);
          color: var(--accent-gold);
        }
        .form-control:focus, .form-select:focus {
          border-color: var(--accent-gold) !important;
          box-shadow: 0 0 0 0.25rem rgba(200, 173, 85, 0.25) !important;
        }
      `}</style>
    </div>
  );
};

export default NuevoVehiculoPage;
