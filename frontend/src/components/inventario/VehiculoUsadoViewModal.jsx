import React from 'react';
import BadgeEstado from '../common/BadgeEstado';

const VehiculoUsadoViewModal = ({ isOpen, onClose, data }) => {
  if (!data) return null;

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value || 0);
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-view-header">
            <h5 className="modal-title fw-bold">Detalles de Evaluación de Usado</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <div className="modal-body modal-view-body">
            <div className="row g-4">
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body">
                    <h6 className="text-muted fw-bold text-uppercase small mb-3">Información del Vehículo</h6>
                    <div className="mb-2"><strong>Vehículo:</strong> {data.vehiculo_detalle}</div>
                    <div className="mb-2"><strong>Taller:</strong> {data.taller_nombre || 'N/A'}</div>
                    <div className="mb-2"><strong>Usuario Autoriza:</strong> {data.usuario_autoriza_nombre}</div>
                    <div className="mb-2"><strong>Fecha Ingreso:</strong> {data.fecha_ingreso}</div>
                    <div className="mb-2"><strong>Fecha Evaluación:</strong> {data.fecha_evaluacion || 'N/A'}</div>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <div className="card border-0 shadow-sm h-100">
                  <div className="card-body">
                    <h6 className="text-muted fw-bold text-uppercase small mb-3">Tasación Financiera</h6>
                    <div className="mb-2"><strong>Precio Info Auto:</strong> {formatCurrency(data.precio_info_auto)}</div>
                    <div className="mb-2"><strong>Deducción:</strong> {data.porcentaje_deduccion}%</div>
                    <div className="mb-2">
                      <strong className="text-success">Precio Tasación Final:</strong>
                      <span className="ms-2 fs-5 fw-bold text-success">{formatCurrency(data.precio_tasacion_final)}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-12">
                <div className="card border-0 shadow-sm">
                  <div className="card-body">
                    <h6 className="text-muted fw-bold text-uppercase small mb-3">Estado de Componentes</h6>
                    <div className="row text-center">
                      <div className="col-3 border-end">
                        <div className="small text-muted">Motor</div>
                        <div className="fw-bold"><BadgeEstado estado={data.estado_motor} /></div>
                      </div>
                      <div className="col-3 border-end">
                        <div className="small text-muted">Cubiertas</div>
                        <div className="fw-bold"><BadgeEstado estado={data.estado_cubierta} /></div>
                      </div>
                      <div className="col-3 border-end">
                        <div className="small text-muted">Chapa/Pintura</div>
                        <div className="fw-bold"><BadgeEstado estado={data.estado_chapa_pintura} /></div>
                      </div>
                      <div className="col-3">
                        <div className="small text-muted">Interior</div>
                        <div className="fw-bold"><BadgeEstado estado={data.estado_interior} /></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-12">
                <div className="card border-0 shadow-sm">
                  <div className="card-body">
                    <h6 className="text-muted fw-bold text-uppercase small mb-3">Observaciones</h6>
                    <p className="text-secondary mb-0 modal-text-wrap">
                      {data.observaciones || 'Sin observaciones adicionales.'}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-footer modal-view-footer">
            <button className="btn btn-secondary px-4" onClick={onClose}>Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehiculoUsadoViewModal;
