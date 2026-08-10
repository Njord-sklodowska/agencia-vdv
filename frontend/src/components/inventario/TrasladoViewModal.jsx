import React from 'react';
import BadgeEstado from '../common/BadgeEstado';

const TrasladoViewModal = ({ isOpen, onClose, data }) => {
  if (!isOpen || !data) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-md modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-view-header">
            <h5 className="modal-title fw-bold">Detalles del Traslado</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <div className="modal-body p-4">
            <div className="text-center mb-4">
              <div className="bg-light d-inline-block p-3 rounded-circle mb-2">
                <i className="bi bi-truck fs-1 text-primary"></i>
              </div>
              <h4 className="fw-bold">{data.vehiculo_detalle}</h4>
              <BadgeEstado estado={data.estado} />
            </div>
            <div className="list-group list-group-flush">
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Origen</span>
                <span className="fw-medium">{data.sucursal_origen_nombre || '---'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Destino</span>
                <span className="fw-medium">{data.sucursal_destino_nombre || '---'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Fecha</span>
                <span className="fw-medium">{data.fecha_traslado || '---'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Costo</span>
                <span className="fw-medium">{new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(data.costo_traslado || 0)}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Motivo</span>
                <span className="fw-medium text-end modal-text-truncate">{data.motivo || 'Sin motivo especificado'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Autoriza</span>
                <span className="fw-medium">{data.usuario_autoriza_nombre || '---'}</span>
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

export default TrasladoViewModal;
